#!/bin/sh
# Baut die statische Seite nach dist/client. Wird lokal und in CI (deploy.yml) genutzt.
# BASE_PATH: Unterpfad der Seite. Eigene Domain (elua-chor.de) am Root: / (Default). Ohne eigene Domain: /elua-website/
set -eu

BASE_PATH="${BASE_PATH:-/}"
export BASE_PATH

npx --yes webstudio@0.298.0 build --template ssg

# webstudio build erzeugt vite.config.ts bei jedem Lauf neu, der Basispfad muss danach nachgetragen werden
sed -i.bak 's|export default defineConfig({|export default defineConfig({\n  base: process.env.BASE_PATH ?? "/",|' vite.config.ts
rm -f vite.config.ts.bak

[ -d node_modules ] || npm ci
npm run build

cp -R static/. dist/client/

git checkout -- vite.config.ts 2>/dev/null || true
