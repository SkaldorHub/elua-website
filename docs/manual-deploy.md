# Manueller Deploy (Fallback)

Für den Fall, dass die GitHub-Actions-Minuten aufgebraucht sind (private Repos: 2000 Min/Monat, öffentliche Repos: unbegrenzt) oder Actions nicht läuft.

1. Aktuellen Stand holen und exportieren:
   ```
   npx webstudio@0.298.0 sync
   sh scripts/build.sh
   ```
   Das Skript baut mit dem Default `BASE_PATH=/elua-website/` und kopiert `static/` in den Export. Das Ergebnis liegt in `dist/client/` (per `.gitignore` nicht im Git). Bei eigener Domain am Root: `BASE_PATH=/ sh scripts/build.sh`.

2. Export auf den `gh-pages`-Branch pushen:
   ```
   npx gh-pages -d dist/client
   ```

3. Pages-Source umstellen: Settings, Pages, Source, "Deploy from a branch", Branch `gh-pages`, Ordner `/ (root)`.

4. Sobald Actions wieder läuft: Source zurück auf "GitHub Actions" stellen (siehe [setup.md](setup.md)).
