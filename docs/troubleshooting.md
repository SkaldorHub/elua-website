# Fehlerbilder und Lösungen

## Website und Deploy

| Symptom | Ursache | Lösung |
|---|---|---|
| Live-Seite ist reiner Text, ohne Design | CSS und JS liegen unter `/assets/…`, die Seite aber unter `/elua-website/`. Alles liefert 404. | Beim Build `BASE_PATH` setzen (macht `scripts/build.sh`). Prüfen: Quelltext der Seite, die CSS-URL muss mit `/elua-website/assets/` beginnen. |
| CI-Lauf schlägt nach 0 Sekunden fehl, Name des Laufs ist der Dateipfad | `deploy.yml` ist kein gültiges YAML (z. B. `: ` in einer einzeiligen `run:`-Zeile) | Mehrzeilige Befehle als Block schreiben (`run: \|`) und lokal prüfen: `python3 -c "import yaml; yaml.safe_load(open('.github/workflows/deploy.yml'))"` |
| `webstudio build`: "Template is not provided" | Template fehlt | `--template ssg` mitgeben (macht `scripts/build.sh`) |
| Bild fehlt nach dem Deploy | Datei nicht in `static/` oder falsche URL im Bild-Element | Datei in `static/` ablegen, URL `https://skaldorhub.github.io/elua-website/<datei>` |
| Änderung in der Cloud, Seite bleibt alt | CI baut nur aus dem Repo | `sync`, Commit, Push (siehe [workflow.md](workflow.md)) |
| Änderung im Repo verschwindet nach Arbeit im Cloud-Editor | Cloud hatte den Repo-Stand nicht, `sync` hat ihn überschrieben | Vor Arbeit in der Cloud Repo-Stand per `import` einspielen (siehe [workflow.md](workflow.md)) |
| `vite.config.ts` zeigt nach lokalem Build eine Änderung | Das Skript trägt den Basispfad nur temporär ein | `git checkout -- vite.config.ts` (das Skript macht das am Ende selbst) |
| Screenshot mit Headless-Chrome ist rechts abgeschnitten | Headless-Chrome hat eine Mindestbreite von etwa 500 px | Am echten Gerät prüfen |

## Webstudio-CLI und Rechte

| Symptom | Ursache | Lösung |
|---|---|---|
| "Authorization token cannot use Builder API" | Dem Link fehlt das API-Recht. Im Cloud-Plan nicht verfügbar. | Betrifft Asset-Upload und `insert-fragment`. Import mit `--skip-assets`, Bilder über `static/`, automatisiertes Einspielen über [selfhost-editing.md](selfhost-editing.md). |
| Import bricht bei Assets ab, Cloud bleibt unverändert | Asset-Upload braucht API-Recht, der Import wird dann komplett abgebrochen | `import --skip-assets` |
| `DESTRUCTIVE_CONFIRMATION_REQUIRED` | Schutz vor versehentlichem Löschen | Aufruf unverändert mit `confirmDestructive: true` und dem zurückgegebenen `confirmationToken` wiederholen (Token läuft schnell ab) |
| Import hat Änderungen anderer überschrieben | `import` ersetzt das ganze Cloud-Projekt | Vorher `sync` und `git diff`. Wiederherstellung über `.webstudio/data.json` aus Git, siehe Rollback. |
| Abstand oder Breite aus einem lokalen Style greift im Export nicht | Token und lokaler Style setzen dieselbe Eigenschaft, im Export gewinnt das Token | Eigenes Token für die Abweichung anlegen, siehe [selfhost-editing.md](selfhost-editing.md) |
| Tokens tauchen doppelt auf (`banner-1`, `section-1`) und alte Eigenschaften bleiben | `apply-design.py` wurde mit geänderten Token-Definitionen erneut ausgeführt | Lokales Projekt zurücksetzen, siehe [selfhost-editing.md](selfhost-editing.md) |

## Lokaler Builder (Selfhost)

| Symptom | Ursache | Lösung |
|---|---|---|
| `Cannot connect to the Docker daemon` oder `docker.sock: no such file` | Docker Desktop läuft nicht | `open -a Docker`, warten bis `docker ps` antwortet |
| Zed: "Failed to start Dev Container" oder "No such container" | Docker war aus, oder Zed hält eine alte Container-ID | Docker starten, Zed beenden und den Ordner neu öffnen |
| Im Container fehlt `psql` | Container wurde mit rohem `docker compose` gebaut | Über Zed/Dev-Container-Tooling bauen lassen |
| `PrismaClientInitializationError` bei Migrationen | Ports in `apps/builder/.env` (55432/55433) passen nicht | Auf 5432 und 3000 ändern, siehe [selfhost-editing.md](selfhost-editing.md) |
| Browser: `PR_CONNECT_RESET_ERROR` oder `PR_END_OF_FILE_ERROR` | Vite bindet auf 127.0.0.1, das bricht TLS über Docker Desktop | `pnpm dev --host 0.0.0.0` |
| Browser: HSTS-Fehler bei `p-<id>.vite.wstd.dev` | Wildcard-Zertifikat deckt nur eine Ebene | `https://wstd.dev:5173` benutzen, nicht `vite.wstd.dev` |
| `can't access property "useRef", dispatcher is null` oder `error loading dynamically imported module … chunk-…` | Vite hat Abhängigkeiten nachoptimiert, der Browser mischt alte und neue Bundles | Hard-Reload, privates Fenster oder Chrome. Im Serverlog steht "optimized dependencies changed". |
| `webstudio permissions` zeigt `canUseApi: no` trotz Token | Plan-Feature `allowAdditionalPermissions` fehlt: Nutzer ohne Pro-Plan oder `PLANS` nicht im Prozess | Pro-Plan sicherstellen, Builder mit `set -a; . ./.env; set +a` neu starten |
| `403` vom Builder auf `curl` | Normale App-Antwort ohne Login, kein Fehler | Im Browser einloggen |
