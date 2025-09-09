Dépanneur — Web service + minimal chat UI
=========================================

Contenu:
- app/main.py        -> FastAPI backend (API + serve UI)
- app/data.json      -> base de données (remplacer par votre data.json complet)
- app/templates/index.html
- app/static/style.css
- app/static/app.js
- requirements.txt
- Procfile

Déploiement local:
python -m venv .venv
source .venv/bin/activate   # ou .venv\Scripts\activate sur Windows
pip install -r requirements.txt
uvicorn app.main:app --reload

Déploiement Render:
- push sur GitHub puis connectez Render
- Build command: pip install -r requirements.txt
- Start command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
