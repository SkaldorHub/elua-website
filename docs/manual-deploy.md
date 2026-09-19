# Manueller Deploy (Fallback)

Falls die GitHub Actions Free-Minuten aufgebraucht sind (privates Repo: 2000 Min/Monat) oder Actions aus anderem Grund nicht läuft.

1. Aktuellen Stand lokal holen und exportieren:
   ```
   npx webstudio sync
   npx webstudio build --template ssg
   sed -i.bak 's|export default defineConfig({|export default defineConfig({\n  base: process.env.BASE_PATH ?? "/",|' vite.config.ts && rm vite.config.ts.bak
   npm ci
   BASE_PATH=/elua-website/ npm run build
   cp -R static/. dist/client/
   ```
   `BASE_PATH` ist der Unterpfad der GitHub-Pages-URL (`https://<user>.github.io/elua-website/`). Bei eigener Domain am Root weglassen. Ohne ihn liefert die Seite 404 auf CSS/JS und erscheint als reiner Text.
   Der Static Export landet in `dist/client/` (siehe `.gitignore` – wird nicht mit dem Quellcode committet)

2. Export auf den `gh-pages`-Branch pushen:
   ```
   npx gh-pages -d dist/client
   ```
   (einmalig `npm i -D gh-pages` falls noch nicht installiert)

3. Pages-Source zurückstellen, falls nötig: Settings → Pages → Source → "Deploy from a branch" → `gh-pages` / `/ (root)`

4. Sobald GitHub Actions wieder verfügbar ist: Source zurück auf "GitHub Actions" stellen (siehe [setup.md](setup.md))
