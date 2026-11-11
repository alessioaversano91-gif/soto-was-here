"""Rigenera index.html a partire da src/SOTO-Was-Here.jsx.
Uso: python3 build.py"""
from pathlib import Path

root = Path(__file__).parent
src = (root / 'src' / 'SOTO-Was-Here.jsx').read_text(encoding='utf-8')
assert '</script' not in src, 'il codice non deve contenere </script'

page = '''<!doctype html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>SOTO Was Here</title>
<meta name="description" content="SOTO WAS HERE: mappa pixel dell'Europa e diorami 3D di Genova, Lione, Mantova e Marsiglia.">
<style>html,body{margin:0;height:100%;background:#0b0a0f;color:#f1eff5;color-scheme:dark}#root{height:100%}</style>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script src="https://unpkg.com/react@18.3.1/umd/react.production.min.js"></script>
<script src="https://unpkg.com/react-dom@18.3.1/umd/react-dom.production.min.js"></script>
<script src="https://unpkg.com/@babel/standalone@7.26.4/babel.min.js"></script>
</head>
<body>
<div id="root"></div>
<script type="text/plain" id="soto-src">''' + src + '''</script>
<script>
(function () {
  try {
    var THREE_UMD = window.THREE;
    var code = document.getElementById('soto-src').textContent;
    code = code.replace(/^import .*$/gm, '').replace('window.THREE = Object.assign({}, THREE_NS);', 'window.THREE = Object.assign({}, THREE_UMD);').replace('export default function App', 'window.__App = function App');
    var out = Babel.transform(code, { presets: ['react'] }).code;
    new Function('React', 'THREE_UMD', out)(React, THREE_UMD);
    ReactDOM.createRoot(document.getElementById('root')).render(React.createElement(window.__App));
  } catch (e) {
    document.body.innerHTML = '<pre style="color:#f1eff5;padding:16px;white-space:pre-wrap">' + e.message + '\\n' + (e.stack || '') + '</pre>';
  }
})();
</script>
</body>
</html>
'''
(root / 'index.html').write_text(page, encoding='utf-8')
print('index.html aggiornato,', len(page), 'caratteri')
