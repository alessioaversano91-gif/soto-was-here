#!/usr/bin/env python3
"""Pubblica i punti SOTO sul sito.

Uso: python3 tools/publish_points.py <cartella con i punti .json esportati dall'artifact> [cartella con le foto scaricate]

- tiene solo i punti con stato "published";
- copia le foto in data/photos/ e riscrive il campo photo con il percorso del sito;
- scrive data/points.json, ordinato per citta e data.
Le foto nell'artifact hanno photo = "/_blob/<id>": il file scaricato deve chiamarsi <id>.<estensione>.
Una foto salvata come data URL viene scritta direttamente su file.
"""
import base64, hashlib, json, shutil, sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent
src = Path(sys.argv[1]); blobs = Path(sys.argv[2]) if len(sys.argv) > 2 else None
photos = root / 'data' / 'photos'; photos.mkdir(parents=True, exist_ok=True)
out, kept, missing = [], set(), []
for f in sorted(src.glob('*.json')):
    p = json.loads(f.read_text(encoding='utf-8'))
    if p.get('status') != 'published' or p.get('lat') is None or p.get('lon') is None:
        continue
    p.setdefault('id', f.stem); ph = p.get('photo') or ''
    if ph.startswith('data:'):
        ext = 'png' if 'png' in ph[:30] else 'webp' if 'webp' in ph[:30] else 'jpg'
        raw = base64.b64decode(ph.split(',', 1)[1]); name = '%s.%s' % (p['id'], ext)
        (photos / name).write_bytes(raw); kept.add(name)
        p['photo'] = 'data/photos/%s?v=%s' % (name, hashlib.sha1(raw).hexdigest()[:8])
    elif ph.startswith('/_blob/'):
        bid = ph.split('/')[-1]; found = sorted(blobs.glob(bid + '.*')) if blobs else []
        if found:
            name = '%s%s' % (p['id'], found[0].suffix.lower() or '.jpg'); shutil.copyfile(found[0], photos / name); kept.add(name)
            p['photo'] = 'data/photos/%s?v=%s' % (name, hashlib.sha1(found[0].read_bytes()).hexdigest()[:8])
        else:
            missing.append((p['id'], bid)); p['photo'] = ''
    out.append(p)
for f in photos.iterdir():
    if f.is_file() and f.name not in kept and f.name != '.gitkeep':
        f.unlink()
out.sort(key=lambda p: (p.get('city', ''), p.get('date', ''), p['id']))
(root / 'data' / 'points.json').write_text(json.dumps(out, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
print('%d punti pubblicati, %d foto' % (len(out), len(kept)))
for pid, bid in missing:
    print('FOTO MANCANTE per il punto %s (%s)' % (pid, bid))
