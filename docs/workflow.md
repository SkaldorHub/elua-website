# Workflow

## Standardweg: im Cloud-Editor ändern

1. Im Webstudio-Cloud-Projekt Inhalt oder Design ändern. Ein "Publish" in Webstudio ist nicht nötig, der CI-Lauf holt den aktuellen Projektstand.
2. Live schalten, eine der beiden Möglichkeiten:
   - GitHub, Tab **Actions**, Workflow **Deploy**, **Run workflow** (schnellster Weg, kein lokaler Schritt)
   - Ein beliebiger Push auf `main`
3. Status prüfen: Tab Actions, grüner Lauf = live (dauert etwa eine Minute).
4. Repo als Sicherung nachziehen:
   ```
   npx webstudio@0.298.0 sync
   git diff --stat            # nur erwartete Änderungen?
   git add .webstudio app pages
   git commit -m "content: <kurz was>"
   git push
   ```
   Commit-Messages sind kurze Einzeiler.

Kein Git-Commit ist nötig, damit die Seite sich ändert. Er hält nur die Historie fest.

## Dateien und Bilder

- **Chorfoto und andere Dateien:** in `static/` ablegen. `scripts/build.sh` kopiert den Ordner in die Seite. Im Bild-Element im Cloud-Editor wird die Datei über ihre volle URL eingetragen: `https://skaldorhub.github.io/elua-website/<dateiname>`. Die feste URL sorgt dafür, dass das Bild auch im Editor sichtbar ist.
- **Warum nicht den Asset-Upload nutzen?** Der Upload über CLI/API braucht das API-Recht, das im Cloud-Plan nicht verfügbar ist. Ein Upload direkt im Cloud-Editor (Assets-Bereich) ist der normale Webstudio-Weg. Er wurde in diesem Projekt bisher nicht mit einem Deploy getestet.
- Bilder vor dem Ablegen verkleinern, z. B. `sips -s format jpeg -s formatOptions 82 -Z 1800 quelle.jpg --out static/name.jpg` (macOS).
- Bei einem Wechsel auf eine eigene Domain die Bild-URL anpassen (siehe [dns-domain.md](dns-domain.md)).

## Lokal prüfen

```
npx webstudio@0.298.0 sync
BASE_PATH=/ sh scripts/build.sh
cd dist/client && python3 -m http.server 8080
```

`BASE_PATH` ist der Unterpfad der Seite. Auf GitHub Pages ohne eigene Domain ist es `/elua-website/` (Default des Skripts und im CI). Ohne den richtigen Wert lädt die Seite kein CSS und JS und erscheint als reiner Text.

## Automatisiertes Bearbeiten

Layout und Texte lassen sich auch per CLI einspielen (`design/*.jsx`). Das braucht einen lokalen Webstudio-Builder mit API-Recht und ist in [selfhost-editing.md](selfhost-editing.md) beschrieben. Für einzelne Textänderungen ist der Cloud-Editor einfacher.

## Rollback

Der CI-Lauf synchronisiert immer aus der Cloud. Ein `git revert` auf `.webstudio/data.json` ändert die Live-Seite deshalb nicht. So gehst du auf einen früheren Stand zurück:

1. Älteren Projektstand aus Git holen: `git checkout <commit> -- .webstudio/data.json`
2. In die Cloud zurückspielen: `npx webstudio@0.298.0 import --skip-assets --to '<cloud-share-link>'`
3. Deploy wie oben auslösen.

Achtung: `import` überschreibt das gesamte Cloud-Projekt. Vorher `sync` und `git diff` ausführen, damit keine fremden Änderungen verloren gehen. Der Mechanismus ist derselbe wie beim Einspielen von Layouts, als Rollback aber nicht gesondert getestet.

## Regeln

- Generierte Dateien (`app/`, `pages/`, `renderer/`, `vite.config.ts`, `package.json`) nicht von Hand bearbeiten. Sie werden bei jedem Build überschrieben.
- Vor Änderungen in der Cloud kurz abstimmen, wenn mehrere Personen gleichzeitig arbeiten. Der Import aus dem Selfhost-Weg überschreibt alles.
