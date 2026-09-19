#!/usr/bin/env python3
"""Spielt design/*.jsx und design/tokens.json in das verlinkte Webstudio-Projekt ein.

Voraussetzung: Das aktuelle Verzeichnis ist mit einem Projekt verlinkt, dessen Link das
API-Recht hat (siehe docs/selfhost-editing.md). Aufruf im Selfhost-Ordner:
    python3 /pfad/zum/repo/scripts/apply-design.py
"""
import json
import re
import subprocess
import sys
from pathlib import Path

CLI = "webstudio@0.298.0"
DESIGN = Path(__file__).resolve().parent.parent / "design"
PAGES = {"": "home.jsx", "/impressum": "impressum.jsx"}


def call(tool, payload, *flags):
    out = subprocess.run(["npx", "--yes", CLI, tool, json.dumps(payload, ensure_ascii=False), *flags],
                         capture_output=True, text=True).stdout
    result = json.JSONDecoder().raw_decode(out[out.index("{"):])[0]
    if not result.get("ok"):
        sys.exit(f"{tool} fehlgeschlagen: {json.dumps(result.get('error'), ensure_ascii=False)[:600]}")
    return result["data"]


def render(jsx, tokens):
    def expand(match):
        names = match.group(1).split()
        unknown = [n for n in names if n not in tokens]
        if unknown:
            sys.exit(f"Unbekannte Tokens in tokens.json: {unknown}")
        return "ws:tokens={[" + ", ".join(f"token('{n}', css`{tokens[n]}`)" for n in names) + "]}"
    return re.sub(r'tokens="([^"]+)"', expand, jsx)


def declarations(css_text):
    return [tuple(part.strip() for part in decl.split(":", 1)) for decl in css_text.split(";") if decl.strip()]


spec = json.loads((DESIGN / "tokens.json").read_text(encoding="utf-8"))
roots = {page["path"]: page["rootInstanceId"] for page in call("list-pages", {})["pages"]}

for path, filename in PAGES.items():
    if path not in roots:
        sys.exit(f"Seite '{path or '/'}' fehlt im Projekt. Erst mit create-page anlegen.")
    payload = {"parentInstanceId": roots[path], "mode": "replace", "conflictResolution": "theirs",
               "fragment": render((DESIGN / filename).read_text(encoding="utf-8").strip(), spec["tokens"])}
    call("insert-fragment", payload, "--dry-run")
    call("insert-fragment", payload)
    print(f"{filename} eingespielt")

breakpoints = {b["label"]: b["id"] for b in call("list-breakpoints", {})["breakpoints"]}
token_ids = {t["name"]: t["id"] for t in call("list-design-tokens", {"withUsage": False, "limit": 200})["tokens"]}

overrides = {}
for label, per_token in spec["responsive"].items():
    for name, css_text in per_token.items():
        for prop, value in declarations(css_text):
            overrides.setdefault(name, []).append({"property": prop, "value": value, "breakpoint": breakpoints[label]})
for name, updates in overrides.items():
    call("update-design-token-styles", {"designTokenId": token_ids[name], "updates": updates})
print(f"{len(overrides)} Tokens mit Breakpoint-Anpassungen")
