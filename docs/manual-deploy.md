# Manueller Deploy (Fallback)

Falls die GitHub Actions Free-Minuten aufgebraucht sind (privates Repo: 2000 Min/Monat) oder Actions aus anderem Grund nicht läuft.

1. Aktuellen Stand lokal holen und exportieren:
   ```
   npx webstudio sync
   npx webstudio build --template ssg
   ```
   Der Static Export landet im `dist/`-Ordner (siehe `.gitignore` – wird nicht mit dem Quellcode committet)

2. Export auf den `gh-pages`-Branch pushen:
   ```
   npx gh-pages -d dist
   ```
   (einmalig `npm i -D gh-pages` falls noch nicht installiert)

3. Pages-Source zurückstellen, falls nötig: Settings → Pages → Source → "Deploy from a branch" → `gh-pages` / `/ (root)`

4. Sobald GitHub Actions wieder verfügbar ist: Source zurück auf "GitHub Actions" stellen (siehe [setup.md](setup.md))
