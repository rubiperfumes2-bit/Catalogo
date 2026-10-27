# Web de Rubí Perfumes

Página pública (GitHub Pages): https://rubiperfumes2-bit.github.io/Catalogo/

- `index.html` se GENERA con `src/build.py`; no editarlo a mano.
- Datos: colección `productos` del Panel Rubí (https://claude.ai/artifact/LftfmN1sEQkXifjq1xJNyR), leída con ArtifactData (`list`, `out_dir`).
- Diseño y textos: `src/tpl.html` (marcador `__DATA__`). Fotos: `src/img/<id>.webp` (sin fondo).
- Perfumes con `linea: 'diseñador'` muestran "Consultá precio". `tipo: 'evaluacion'` no se publica.
- Commits en español, cortos.

## Actualizar
1. Bajar productos: ArtifactData list `productos` con `out_dir` → carpeta P.
2. `python3 -I src/build.py P` → si dice `MISSING_IMG <ids>`, bajar esas fotos con Artifact read (`path` = id del blob de `img`) a una carpeta B y correr `python3 -I src/build.py P B`.
3. Si `git diff --quiet index.html` da cambios: commit + push a `main`.
