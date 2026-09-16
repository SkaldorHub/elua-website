# Workflow (Alltag)

1. Website in Webstudio Cloud bearbeiten, Änderungen dort publishen
2. Lokal syncen und committen:
   ```
   npx webstudio sync
   git add .
   git commit -m "sync: <kurzbeschreibung>"
   git push
   ```
3. Push auf `main` triggert automatisch den Deploy-Workflow (`.github/workflows/deploy.yml`)
4. Status prüfen: GitHub Repo → Tab "Actions" → letzter Lauf grün = live

Kein manueller Build/Export nötig, solange GitHub Actions verfügbar ist.
