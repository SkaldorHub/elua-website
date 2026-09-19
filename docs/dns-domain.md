# Eigene Domain bei IONOS

Solange keine eigene Domain eingerichtet ist, läuft die Seite unter `https://skaldorhub.github.io/elua-website/` (Unterpfad `/elua-website/`).

## DNS bei IONOS

1. In der DNS-Verwaltung der Domain setzen:
   - A-Records für die Root-Domain auf die vier GitHub-IPs:
     - `185.199.108.153`
     - `185.199.109.153`
     - `185.199.110.153`
     - `185.199.111.153`
   - Optional AAAA-Records (IPv6):
     - `2606:50c0:8000::153`
     - `2606:50c0:8001::153`
     - `2606:50c0:8002::153`
     - `2606:50c0:8003::153`
   - CNAME-Record für `www` auf `<github-username>.github.io`
2. Im Repo unter Settings, Pages die Custom Domain eintragen. GitHub prüft die DNS-Einträge und aktiviert HTTPS (bis zu 24 Stunden). Eine `CNAME`-Datei ist beim Deploy über GitHub Actions nicht nötig, die Domain wird in den Settings hinterlegt.
3. "Enforce HTTPS" aktivieren, sobald verfügbar.

## Anpassungen im Projekt beim Wechsel auf die Domain

Auf einer eigenen Domain liegt die Seite am Root, nicht mehr unter `/elua-website/`. Ohne diese Anpassungen fehlen CSS und JS:

1. `.github/workflows/deploy.yml`, Schritt **Build**: `BASE_PATH: /${{ github.event.repository.name }}/` ändern in `BASE_PATH: /`
2. Im Skript `scripts/build.sh` den Default `/elua-website/` auf `/` setzen (oder beim manuellen Bauen `BASE_PATH=/` mitgeben).
3. Im Cloud-Editor die Bild-URL des Chorfotos auf die neue Domain ändern: `https://<deine-domain>/elua-chor.jpg`. Die alte github.io-URL leitet zwar weiter, sollte aber nicht auf Dauer benutzt werden.
4. Die Links im Footer und auf der Impressum-Seite (`impressum/`, `../`) sind relativ und brauchen keine Änderung.
