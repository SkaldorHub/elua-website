# Setup für neue Mitarbeitende

## Voraussetzungen

- Node.js ≥ 22 (`node --version`), git
- Zugang zum GitHub-Repo (Collaborator)
- Einladung ins Webstudio-Cloud-Projekt (Share/Invite im Projekt), damit du im Editor arbeiten kannst

## Lokal einrichten

1. Repo holen und Abhängigkeiten installieren:
   ```
   git clone https://github.com/SkaldorHub/elua-website.git
   cd elua-website
   npm ci
   ```
2. Share-Link für die CLI holen: im Cloud-Projekt oben rechts **Share**, dann einen Link mit der Rolle **Builder** anlegen (Name z. B. `cli-<dein-name>`) und kopieren.
   Ein solcher Link ist ein Zugangsschlüssel. Nicht in Chats, Tickets oder Git posten.
3. Repo mit dem Projekt verlinken:
   ```
   npx webstudio@0.298.0 link --link '<share-link>'
   ```
   Der Token landet im Benutzerverzeichnis (macOS: `~/Library/Preferences/webstudio-nodejs/`), nicht im Repo. `.webstudio/config.json` enthält nur die Projekt-ID und ist eingecheckt.
4. Stand holen und prüfen:
   ```
   npx webstudio@0.298.0 sync
   git status
   ```
   Der Arbeitsbaum sollte sauber sein. Falls nicht, hat jemand in der Cloud etwas geändert, das noch nicht committet ist.
5. Lokal bauen und ansehen:
   ```
   BASE_PATH=/ sh scripts/build.sh
   cd dist/client && python3 -m http.server 8080
   ```
   Dann http://localhost:8080. Das Chorfoto wird von der Live-URL geladen (siehe [workflow.md](workflow.md)).

## Einmalig durch die Repo-Betreuung

- GitHub Actions Secret setzen: `gh secret set WEBSTUDIO_LINK` (fragt den Wert interaktiv ab, landet nicht in der Shell-History). Wert ist ein Builder-Share-Link des Cloud-Projekts.
- GitHub Pages auf "GitHub Actions" stellen: Settings, Pages, Source, GitHub Actions.
- Wird der Share-Link ersetzt (z. B. weil er bekannt geworden ist): alten Link im Webstudio-Share-Dialog löschen, neuen anlegen und das Secret neu setzen.

## Versionen

Die Webstudio-CLI ist auf `0.298.0` festgepinnt, an drei Stellen: `scripts/build.sh`, `.github/workflows/deploy.yml` (link und sync) und diese Doku. Bei einem Update alle gemeinsam anheben und einmal lokal bauen.
