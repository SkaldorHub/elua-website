# Elua Website

Vereins-Website: Design/Content-Pflege im [Webstudio](https://webstudio.is) Cloud-Editor, dieses Repo hält die versionierte Sync-Kopie und deployt automatisch auf GitHub Pages.

## Architektur

```mermaid
flowchart LR
    A[Webstudio Cloud Editor] -->|webstudio sync| B[dieses Repo]
    B -->|push main| C[GitHub Actions]
    C -->|webstudio build| D[Static Export]
    D -->|deploy-pages| E[GitHub Pages]
    E -->|A/AAAA/CNAME| F[Custom Domain via IONOS]
```

## Docs

- [docs/setup.md](docs/setup.md) – einmaliges Setup
- [docs/workflow.md](docs/workflow.md) – laufender Redaktionsalltag
- [docs/manual-deploy.md](docs/manual-deploy.md) – Fallback ohne GitHub Actions
- [docs/dns-domain.md](docs/dns-domain.md) – DNS-Einrichtung bei IONOS
