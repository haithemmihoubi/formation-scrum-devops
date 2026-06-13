# Cours : Dockeriser ses applications (multi-stage & multi-environnement)

Support de formation DevOps couvrant la dockerisation des applications **Spring Boot,
Angular, React et Python**, avec build **multi-stage** et gestion **multi-environnement**.

## Contenu

| Module | Sujet |
|--------|-------|
| 00 | Introduction : Docker & le build multi-stage |
| 01 | Java Spring Boot multi-stage (Maven, Gradle, layered jars) |
| 02 | Multi-environnement (profiles, `.env`, `compose.override`, `ARG`/`ENV`) |
| 03 | Angular (multi-stage + Nginx + routage SPA) |
| 04 | React (Vite / CRA + Nginx) |
| 05 | Python (Flask / FastAPI / Django) |
| 06 | Bonnes pratiques, sécurité & checklist |

## Générer le PDF

Prérequis (déjà présents sur la machine de formation) :

```bash
pip install markdown weasyprint
```

Puis :

```bash
python3 build_pdf.py
# → Cours-Docker-Multistage.pdf
```

Chaque module est un fichier `.md` autonome : on peut les éditer puis relancer
`build_pdf.py` pour régénérer le PDF (23 pages, A4).
