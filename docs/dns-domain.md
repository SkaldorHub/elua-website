# DNS-Setup bei IONOS

1. CNAME-Datei im Repo-Root des Export-Ordners mit Domain-Inhalt anlegen (z. B. `elua-chor.de`) – GitHub Pages nutzt sie automatisch
2. Bei IONOS (DNS-Verwaltung der Domain) folgende Einträge setzen:
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
3. Im Repo unter Settings → Pages die Custom Domain eintragen; GitHub prüft die DNS-Einträge automatisch und aktiviert HTTPS (bis zu 24h)
4. "Enforce HTTPS" aktivieren, sobald verfügbar
