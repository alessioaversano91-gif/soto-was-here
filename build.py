"""Rigenera index.html a partire da src/SOTO-Was-Here.jsx.
Uso: python3 build.py [--artifact percorso.html]

Per caricare in fretta, la pagina non traduce piu il codice nel browser:
- i blocchi di dati grandi vengono spostati in uno <script> a parte (non passano dal traduttore);
- il JSX viene tradotto qui, una volta, con Babel (serve node con @babel/standalone:
  cartella indicata da SOTO_BABEL, altrimenti /home/claude/scratch-npm).
Se node o Babel mancano, si ricade sulla pagina che traduce nel browser."""
import json, os, re, subprocess, sys
from pathlib import Path

root = Path(__file__).parent
src = (root / 'src' / 'SOTO-Was-Here.jsx').read_text(encoding='utf-8')
assert '</script' not in src, 'il codice non deve contenere </script'

LIBS = '''<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script src="https://unpkg.com/react@18.3.1/umd/react.production.min.js"></script>
<script src="https://unpkg.com/react-dom@18.3.1/umd/react-dom.production.min.js"></script>
'''
ERR = '''document.body.innerHTML = '<pre style="color:#f1eff5;padding:16px;white-space:pre-wrap">' + e.message + '\\n' + (e.stack || '') + '</pre>';'''
PREP = lambda c: re.sub(r'^import .*$', '', c, flags=re.M).replace('window.THREE = Object.assign({}, THREE_NS);', 'window.THREE = Object.assign({}, THREE_UMD);').replace('export default function App', 'window.__App = function App')

def compiled():
    """Sposta i dati grandi fuori dal codice e traduce il JSX. Restituisce (dati, codice) oppure None."""
    data, lines = [], []
    for ln in src.split('\n'):
        m = re.match(r'^(\s*)const (\w+) = (.*);$', ln) if len(ln) > 20000 else None
        if m:
            data.append('%s:%s' % (json.dumps(m.group(2)), m.group(3)))
            lines.append('%sconst %s = window.__SOTO_DATA.%s;' % (m.group(1), m.group(2), m.group(2)))
        else:
            lines.append(ln)
    node_dir = os.environ.get('SOTO_BABEL', '/home/claude/scratch-npm')
    js = "const B=require('@babel/standalone');let c='';process.stdin.on('data',d=>c+=d).on('end',()=>process.stdout.write(B.transform(c,{presets:['react'],compact:false}).code));"
    try:
        out = subprocess.run(['node', '-e', js], input=PREP('\n'.join(lines)).encode(), capture_output=True, cwd=node_dir, check=True).stdout.decode()
    except Exception as e:
        print('Babel non disponibile (%s): pagina con traduzione nel browser' % type(e).__name__)
        return None
    assert '</script' not in out
    return 'window.__SOTO_DATA={' + ','.join(data) + '};', out

def body(extra=''):
    c = compiled()
    if c:
        return LIBS, '<div id="root"></div>\n<script>' + c[0] + '</script>\n' + extra + '<script>\n(function (React, THREE_UMD) {\n  try {\n' + c[1] + '\n    ReactDOM.createRoot(document.getElementById(\'root\')).render(React.createElement(window.__App));\n  } catch (e) {\n    ' + ERR + '\n  }\n})(window.React, window.THREE);\n</script>\n'
    return LIBS + '<script src="https://unpkg.com/@babel/standalone@7.26.4/babel.min.js"></script>\n', '<div id="root"></div>\n<script type="text/plain" id="soto-src">' + src + '</script>\n' + extra + '''<script>
(function () {
  try {
    var THREE_UMD = window.THREE;
    var code = document.getElementById('soto-src').textContent;
    code = code.replace(/^import .*$/gm, '').replace('window.THREE = Object.assign({}, THREE_NS);', 'window.THREE = Object.assign({}, THREE_UMD);').replace('export default function App', 'window.__App = function App');
    var out = Babel.transform(code, { presets: ['react'] }).code;
    new Function('React', 'THREE_UMD', out)(React, THREE_UMD);
    ReactDOM.createRoot(document.getElementById('root')).render(React.createElement(window.__App));
  } catch (e) {
    ''' + ERR + '''
  }
})();
</script>
'''

STYLE = '<style>html,body{margin:0;height:100%;background:#0b0a0f;color:#f1eff5;color-scheme:dark}#root{height:100%}</style>\n'
libs, bd = body()
page = '''<!doctype html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>SOTO Was Here</title>
<meta name="description" content="SOTO WAS HERE: mappa pixel dell'Europa e diorami 3D di Genova, Lione, Mantova e Marsiglia.">
''' + STYLE + libs + '</head>\n<body>\n' + bd + '</body>\n</html>\n'
(root / 'index.html').write_text(page, encoding='utf-8')
print('index.html aggiornato,', len(page), 'caratteri')

if '--artifact' in sys.argv:
    # Versione per l'artifact di Claude: stessa pagina, piu l'avviso al posto di alert().
    TOAST = '''<script>
/* Nel visualizzatore degli artifact alert() non viene mostrato: lo sostituisco con un avviso nella pagina. */
window.alert = function (msg) {
  var el = document.getElementById('soto-toast');
  if (!el) { el = document.createElement('div'); el.id = 'soto-toast'; el.setAttribute('role', 'alert'); el.style.cssText = 'position:fixed;left:50%;bottom:calc(24px + env(safe-area-inset-bottom,0px));transform:translateX(-50%);z-index:9999;max-width:min(420px,calc(100% - 32px));padding:12px 16px;border-radius:10px;background:#0b0a0f;border:1px solid #ef6b4a;color:#f1eff5;font:14px/1.4 system-ui,sans-serif;box-shadow:0 8px 24px rgba(0,0,0,.5)'; document.body.appendChild(el); }
  el.textContent = String(msg); el.hidden = false; clearTimeout(el._t); el._t = setTimeout(function () { el.hidden = true; }, 4500);
};
</script>
'''
    libs2, bd2 = body(TOAST)
    out = Path(sys.argv[sys.argv.index('--artifact') + 1])
    out.write_text('<title>SOTO Was Here</title>\n' + STYLE + libs2 + bd2, encoding='utf-8')
    print(out.name, 'aggiornato,', out.stat().st_size, 'byte')
