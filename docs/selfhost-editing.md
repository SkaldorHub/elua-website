# Automatisiertes Bearbeiten über einen lokalen Webstudio-Builder

Fortgeschritten, nur nötig, wenn Layout oder Texte per CLI eingespielt werden sollen. Für normale Änderungen reicht der Cloud-Editor.

## Warum überhaupt

Die Webstudio-CLI kann Inhalte einfügen (`insert-fragment`), braucht dafür aber das Recht "API" am Share-Link. Im Cloud-Plan ist die Checkbox "API" im Share-Dialog ausgegraut, dort gibt es das Recht nicht. Der lokal selbst gehostete Builder hat keinen Bezahlplan und schaltet es frei. Die fertigen Änderungen werden anschließend per `import` in das Cloud-Projekt übertragen. Der Import braucht nur Builder-Rechte.

```mermaid
flowchart LR
    J[design/*.jsx] -->|insert-fragment| L[Lokaler Builder, Projekt test]
    L -->|webstudio sync| B[Bundle]
    B -->|webstudio import --skip-assets| C[Cloud-Projekt]
    C -->|Deploy| P[GitHub Pages]
```

## Einmalige Einrichtung

Voraussetzungen: Docker Desktop, Zed oder VS Code mit Dev Containers, ein Fork oder Clone von `webstudio-is/webstudio` (z. B. `~/IdeaProjects/webstudio`).

1. Docker Desktop starten (`open -a Docker`). In Docker Desktop, Settings, Resources, Network, **Enable host networking** aktivieren. Ob das zwingend nötig ist, wurde nicht getrennt geprüft.
2. Den Webstudio-Ordner in Zed öffnen und den Dev-Container starten lassen. Zed führt `postCreateCommand` (`pnpm install`, `pnpm build`, Migrationen) aus, das dauert einige Minuten. Den Container nicht mit rohem `docker compose` starten: Dann fehlen die Dev-Container-Features (z. B. `psql`), und Zed hängt an einer toten Container-ID.
3. In `apps/builder/.env` die Ports an den Dev-Container anpassen (die mitgelieferten Werte passen nicht):
   ```
   DATABASE_URL=postgresql://supabase_admin:pass@localhost:5432/webstudio?pgbouncer=true
   DIRECT_URL=postgresql://supabase_admin:pass@localhost:5432/webstudio
   PGPORT=5432
   POSTGREST_URL=http://localhost:3000
   POSTGREST_PORT=3000
   ```
4. Builder im Container starten (Terminal in Zed):
   ```
   cd apps/builder
   set -a; . ./.env; set +a
   pnpm dev --host 0.0.0.0
   ```
   - `--host 0.0.0.0` ist nötig: Der Standard bindet auf 127.0.0.1, und dann bricht der TLS-Verbindungsaufbau über die Docker-Desktop-Portweiterleitung ab.
   - `. ./.env` ist nötig, damit die Plan-Definition (`PLANS`) im Prozess ankommt. Ohne sie bleibt das API-Recht aus.
5. Im Browser (Chrome empfohlen) `https://wstd.dev:5173/dashboard` öffnen. **Nicht** `vite.wstd.dev`: Das Zertifikat deckt die Projekt-Subdomain `p-<id>.vite.wstd.dev` nicht ab. Beim ersten Laden Hard-Reload (Cmd+Shift+R) oder ein privates Fenster, weil Vite Abhängigkeiten nachoptimiert.
6. "Login with Secret" mit `0000` (`AUTH_SECRET` aus `.env`). Falls das Formular eine Plan-Auswahl hat, **Pro** wählen.
7. Im Dashboard ein neues Projekt anlegen (z. B. `test`) und dessen Projekt-ID merken (steht in der URL als `p-<id>`).

## API-Token anlegen

Der Share-Dialog des lokalen Builders zeigt "API" ebenfalls grau, wenn kein Plan greift. Der Token wird deshalb direkt in der lokalen Wegwerf-Datenbank angelegt:

```
docker exec webstudio_devcontainer-app-1 sh -c "PGPASSWORD=pass psql -h localhost -U supabase_admin -d webstudio -c \"insert into \\\"AuthorizationToken\\\" (token, \\\"projectId\\\", name, relation, \\\"canUseApi\\\") values (gen_random_uuid()::text, '<PROJEKT-ID>', 'cli', 'builders', true) returning token;\""
```

Link-Format: `https://p-<PROJEKT-ID>.wstd.dev:5173/?authToken=<TOKEN>`

In einem **separaten Ordner außerhalb dieses Repos** verlinken, damit die Verlinkung des Repos auf die Cloud erhalten bleibt:

```
mkdir ~/elua-selfhost && cd ~/elua-selfhost
npx webstudio@0.298.0 link --link '<link>'
npx webstudio@0.298.0 permissions        # muss canUseApi: yes zeigen
```

Zeigt es `canUseApi: no`: Plan des Nutzers prüfen (Tabellen `Product`, `TransactionLog`, View `UserProduct` müssen einen Pro-Plan enthalten) und den Builder mit geladener `.env` neu starten (Schritt 4).

## Layout einspielen

1. Seiten und Root-Instanz-ID abfragen: `npx webstudio@0.298.0 list-pages '{}'`. Die `rootInstanceId` der Home-Seite ist der `parentInstanceId`. Sie ist pro Projekt anders.
2. Fragment als JSON bauen (`parentInstanceId`, `fragment` mit dem Inhalt von `design/home.jsx`, `mode: "replace"`) und zuerst mit `--dry-run` prüfen:
   ```
   npx webstudio@0.298.0 insert-fragment --input-file .temp/insert-fragment.json --dry-run
   npx webstudio@0.298.0 insert-fragment --input-file .temp/insert-fragment.json
   ```
3. Weitere Seiten mit `create-page` anlegen, Titel und Beschreibung mit `update-page` setzen.
4. Löschende Aktionen (`delete-props` u. Ä.) liefern `DESTRUCTIVE_CONFIRMATION_REQUIRED` mit einem kurzlebigen Token. Den Aufruf unverändert mit `confirmDestructive: true` und `confirmationToken` wiederholen.

Das Bild-Element bekommt seine `src` als feste URL (siehe [workflow.md](workflow.md)). Ein Asset-Upload in die Cloud scheitert mit "Authorization token cannot use Builder API".

## Zurück in die Cloud

1. **Erst prüfen, ob in der Cloud jemand etwas geändert hat:** im Repo `npx webstudio@0.298.0 sync` und `git status`. Es darf nichts Unerwartetes auftauchen, denn der Import überschreibt das gesamte Cloud-Projekt.
2. Im Selfhost-Ordner: `npx webstudio@0.298.0 sync`
3. Import: `npx webstudio@0.298.0 import --skip-assets --to '<cloud-share-link>'`. `--skip-assets`, weil der Asset-Upload das API-Recht bräuchte.
4. Im Repo: `sync`, `sh scripts/build.sh`, committen, pushen (siehe [workflow.md](workflow.md)).

Cloud-Share-Links nicht in Chats oder Tickets einfügen. Wenn es doch passiert ist, den Link im Share-Dialog löschen, neu anlegen und das Secret `WEBSTUDIO_LINK` erneuern.
