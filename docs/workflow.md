# Workflow

## Grundregel

Die Live-Seite wird **nur aus dem Repo** gebaut (`.webstudio/data.json` auf `main`). Jeder Push auf `main` deployt. Die Webstudio-Cloud ist der Editor, nicht die Quelle.

Cloud und Repo müssen deshalb gleich sein, bevor jemand arbeitet:
- Vor einer Änderung im Cloud-Editor: `git pull`, dann `npx webstudio@0.298.0 sync` in einer Kopie und `git diff`. Gibt es Unterschiede, stehen im Repo neuere Änderungen: erst per `import` in die Cloud spielen (siehe Rollback, Schritt 2), sonst überschreibt der nächste `sync` sie.
- Eine Änderung nur im Repo (z. B. `data.json` von Hand) geht beim Push live, fehlt aber in der Cloud, bis sie per `import` eingespielt ist.

## Standardweg: im Cloud-Editor ändern

1. Im Webstudio-Cloud-Projekt Inhalt oder Design ändern. Ein "Publish" in Webstudio ist nicht nötig.
2. Stand ins Repo holen und live schalten:
   ```
   npx webstudio@0.298.0 sync
   git diff --stat            # nur erwartete Änderungen?
   git add .webstudio app pages
   git commit -m "content: <kurz was>"
   git push
   ```
   Commit-Messages sind kurze Einzeiler.
3. Status prüfen: Tab Actions, grüner Lauf = live (dauert etwa eine Minute).

Ohne Commit und Push ändert sich die Seite nicht.

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

Ein `git revert` auf `main` ändert die Live-Seite direkt. Danach die Cloud nachziehen, damit dort nicht auf dem alten Stand weitergearbeitet wird:

1. `git revert <commit>` und `git push`
2. In die Cloud zurückspielen: `npx webstudio@0.298.0 import --skip-assets --to '<cloud-share-link>'`

Achtung: `import` überschreibt das gesamte Cloud-Projekt. Vorher `sync` in einer Kopie und `git diff`, damit keine fremden Änderungen verloren gehen.

## Regeln

- Generierte Dateien (`app/`, `pages/`, `renderer/`, `vite.config.ts`, `package.json`) nicht von Hand bearbeiten. Sie werden bei jedem Build überschrieben.
- Vor Änderungen in der Cloud kurz abstimmen, wenn mehrere Personen gleichzeitig arbeiten. Der Import aus dem Selfhost-Weg überschreibt alles.
