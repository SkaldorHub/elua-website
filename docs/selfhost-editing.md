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

## Design einspielen

Das Design liegt als Quelle im Repo:

| Datei | Inhalt |
|---|---|
| `design/tokens.json` | Alle Design-Tokens (Farben, Typografie, Abstände, Karten) und ihre Anpassungen für Tablet, Mobile landscape und Mobile portrait |
| `design/home.jsx` | Startseite. Elemente verweisen nur per `tokens="name1 name2"` auf Tokens |
| `design/impressum.jsx` | Impressum, bewusst schlicht |
| `scripts/apply-design.py` | Spielt alles in das verlinkte Projekt ein |

Aufruf im Selfhost-Ordner (dort ist das lokale Projekt verlinkt):

```
python3 /pfad/zum/repo/scripts/apply-design.py
```

Das Skript fragt Seiten, Breakpoints und Token-IDs selbst ab (keine IDs hart codiert), ersetzt den Seiteninhalt (`insert-fragment`, Dry-Run vorher) und trägt danach die Breakpoint-Anpassungen an den Tokens ein. Die Seiten `/` und `/impressum` müssen im Projekt existieren (sonst vorher `create-page`).

Regeln, die sich aus Fehlversuchen ergeben haben:

- **Lokale Styles überschreiben Tokens im Export nicht.** Wer an einem Element eine Eigenschaft setzt, die auch ein Token dort setzt, verliert im gebauten Ergebnis gegen das Token. Deshalb Abweichungen als eigenes Token anlegen (z. B. `pt-sm`, `pb-xl`, `narrow`, `text-last`) und nie dieselbe Eigenschaft in Token und lokal setzen.
- **Token-Definitionen lassen sich per Skript nicht nachträglich ändern.** Ein zweiter Lauf mit geänderten Definitionen legt Kopien wie `banner-1` an und lässt alte Eigenschaften stehen, und es gibt kein Tool zum Löschen von Tokens. Wer bestehende Tokens ändert, setzt vorher das lokale Projekt zurück:
  1. Einen tokenfreien Projektstand aus der Git-Historie holen (z. B. den Stand vor der Token-Einführung: `git show e4c8ad9:.webstudio/data.json`) und im Selfhost-Ordner als `.webstudio/data.json` ablegen
  2. `npx webstudio@0.298.0 import --skip-assets --to '<lokaler-link>'` (ersetzt den lokalen Projektinhalt, der lokale Link braucht dafür nur Builder-Recht)
  3. Danach `apply-design.py` frisch ausführen
  Neue Tokens hinzufügen geht dagegen ohne Reset.
- Ein Cloud-Import ersetzt das gesamte Cloud-Projekt, also auch Token-Änderungen, die jemand im Builder gemacht hat (siehe [content.md](content.md), Abschnitt Design).

## Zurück in die Cloud

1. **Erst prüfen, ob in der Cloud jemand etwas geändert hat:** im Repo `npx webstudio@0.298.0 sync` und `git status`. Es darf nichts Unerwartetes auftauchen, denn der Import überschreibt das gesamte Cloud-Projekt.
2. Im Selfhost-Ordner: `npx webstudio@0.298.0 sync`
3. Import: `npx webstudio@0.298.0 import --skip-assets --to '<cloud-share-link>'`. `--skip-assets`, weil der Asset-Upload das API-Recht bräuchte.
4. Im Repo: `sync`, `sh scripts/build.sh`, committen, pushen (siehe [workflow.md](workflow.md)).

Cloud-Share-Links nicht in Chats oder Tickets einfügen. Wenn es doch passiert ist, den Link im Share-Dialog löschen, neu anlegen und das Secret `WEBSTUDIO_LINK` erneuern.
