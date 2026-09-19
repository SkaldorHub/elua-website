# Deploy ohne Pipeline (getestet)

Für den Fall, dass GitHub Actions nicht läuft oder die Minuten aufgebraucht sind (private Repos: 2000 Min/Monat, öffentliche Repos: unbegrenzt). Der Ablauf wurde am 2026-09-19 einmal komplett durchgespielt: Export auf den Branch `gh-pages`, Pages-Quelle umgestellt, Seite, Impressum, Foto und CSS lieferten 200.

## Ablauf

1. Stand holen und bauen:
   ```
   npx webstudio@0.298.0 sync
   sh scripts/build.sh
   ```
   Das Skript baut mit `BASE_PATH=/elua-website/` und kopiert `static/` in den Export (`dist/client/`). Bei eigener Domain am Root: `BASE_PATH=/ sh scripts/build.sh`.

2. Export auf den Branch `gh-pages` legen. `.nojekyll` verhindert, dass GitHub die Dateien mit Jekyll verarbeitet:
   ```
   touch dist/client/.nojekyll
   npx gh-pages@6 -d dist/client --dotfiles -m "manual deploy"
   ```

3. Pages-Quelle auf den Branch stellen (einmalig pro Wechsel), entweder in Settings, Pages, Source, "Deploy from a branch", `gh-pages` und `/ (root)`, oder per CLI:
   ```
   gh api -X PUT repos/SkaldorHub/elua-website/pages -f build_type=legacy -f 'source[branch]=gh-pages' -f 'source[path]=/'
   ```
   Wurde der Branch schon vor dem Umschalten gepusht, startet kein Build von selbst. Dann anstoßen und warten, bis der Status `built` ist:
   ```
   gh api -X POST repos/SkaldorHub/elua-website/pages/builds
   gh api repos/SkaldorHub/elua-website/pages/builds/latest -q '.status'
   ```
   Danach jeden weiteren manuellen Deploy nur noch mit Schritt 1 und 2, jeder Push auf `gh-pages` löst den Build aus.

4. Zurück auf die Pipeline, sobald Actions wieder verfügbar ist:
   ```
   gh api -X PUT repos/SkaldorHub/elua-website/pages -f build_type=workflow
   ```
   Danach einen Push auf `main` oder "Run workflow" auslösen. Der Branch `gh-pages` wird dann nicht mehr gebraucht und kann gelöscht werden (`git push origin --delete gh-pages`).

## Privates Repo und GitHub Pages

- Pages aus einem **privaten** Repo gibt es nur mit einem bezahlten GitHub-Plan (Pro, Team, Enterprise). Auf GitHub Free ist Pages nur für **öffentliche** Repos verfügbar. Wird das Repo dort privat gestellt, geht die Seite offline.
- Mit bezahltem Plan bleibt die veröffentlichte Seite öffentlich im Internet erreichbar, auch wenn das Repo privat ist (private Zugriffskontrolle für Pages gibt es nur bei Enterprise Cloud).
- Plan prüfen: https://github.com/settings/billing/plans
