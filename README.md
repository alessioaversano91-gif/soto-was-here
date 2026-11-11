# SOTO Was Here

Il sito della crew SOTO (Albi, Seba, Lollo, Alecio): mappa pixel dell'Europa e diorami 3D di Genova, Lione, Mantova e Marsiglia, in italiano e inglese.

**Sito online:** https://alessioaversano91-gif.github.io/soto-was-here/

## File

- `src/SOTO-Was-Here.jsx`: il codice del sito (un unico componente React, motore 3D con Three.js). È il file da modificare.
- `index.html`: la pagina pubblicata. Si rigenera dal `.jsx` con `python3 build.py`.
- `build.py`: script che crea `index.html` dal `.jsx`.

## Note

- Le mappe delle città sono già incluse nel codice (dati OpenStreetMap / OpenFreeMap e altimetrie Terrarium), quindi si aprono senza scaricare nulla.
- Su GitHub Pages i punti dell'Editor restano nel browser e si perdono ricaricando la pagina. Per salvarli si usa Editor → Esporta JSON; i punti da mostrare a tutti vanno inseriti nel codice.
- Mappe © OpenStreetMap contributors. Terreno: Mapzen / AWS Terrain Tiles.
