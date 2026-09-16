# Setup (einmalig)

1. Node ≥ 22 sicherstellen: `node --version`
2. Webstudio-Projekt auf [webstudio.is](https://webstudio.is) anlegen (GitHub-Login), Vereinsmitglieder einladen
3. Repo-Root verlinken:
   ```
   npx --yes webstudio@0.298.0 link
   ```
   Fragt nach dem Link aus dem Webstudio-Projekt (Share/Invite → Link kopieren)
4. Ersten Sync durchführen und committen:
   ```
   npx webstudio sync
   git add .
   git commit -m "initial webstudio sync"
   ```
5. Webstudio Share-Link (aus dem Builder → Share-Dialog) als GitHub Repo-Secret hinterlegen: `gh secret set WEBSTUDIO_LINK` (fragt interaktiv nach dem Wert, landet nie in der Shell-History oder im Repo)
6. GitHub Pages auf "GitHub Actions" als Quelle umstellen: Settings → Pages → Source → GitHub Actions
