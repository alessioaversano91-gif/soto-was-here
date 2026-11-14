# SOTO Was Here

Il sito della crew SOTO (Albi, Seba, Lollo, Alecio): mappa pixel dell'Europa e diorami 3D di Genova, Lione, Mantova e Marsiglia, in italiano e inglese.

**Sito online:** https://alessioaversano91-gif.github.io/soto-was-here/

## File

- `src/SOTO-Was-Here.jsx`: il codice del sito (un unico componente React, motore 3D con Three.js). È il file da modificare.
- `index.html`: la pagina pubblicata. Si rigenera dal `.jsx` con `python3 build.py`.
- `build.py`: script che crea `index.html` dal `.jsx`.
- `CHECKLIST.md`: cosa è stato fatto e cosa manca.

## Note

- Le mappe delle città sono già incluse nel codice (dati OpenStreetMap / OpenFreeMap e altimetrie Terrarium), quindi si aprono senza scaricare nulla.
- **Punti SOTO:** si aggiungono e si modificano nell'Editor dell'artifact su claude.ai, dove si salvano con le foto. Il sito pubblico li legge da `data/points.json` (foto in `data/photos/`) e non mostra l'Editor. Per aggiornare il sito: chiedere a Claude «pubblica i punti»; vengono pubblicati solo quelli con stato «pubblicato».
- `tools/publish_points.py`: script usato per la pubblicazione (prende i punti esportati dall'artifact e scrive `data/points.json`).
- Mappe © OpenStreetMap contributors. Terreno: Mapzen / AWS Terrain Tiles.
