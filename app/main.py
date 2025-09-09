
import json
from pathlib import Path
from fastapi import FastAPI

app = FastAPI()

# chemin vers ton fichier
DATA_PATH = Path(__file__).parent / "data" / "data.json"

with open(DATA_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

@app.get("/data")
def get_data():
    return data
import os, json
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI(title="Dépanneur API")

BASE_DIR = os.path.dirname(__file__)
# servir static (CSS/JS)
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# charger data.json (UTF-8)
DATA_FILE = os.path.join(BASE_DIR, "data.json")
with open(DATA_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

# page web principale (UI)
@app.get("/", response_class=HTMLResponse)
def web_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# API classiques
@app.get("/api/devices")
def list_devices():
    units = data.get("units", [])
    devices = [{"category": u.get("category"), "device": u.get("device")} for u in units]
    return JSONResponse(content=devices)

@app.get("/api/device/{device_name}")
def get_device(device_name: str):
    units = data.get("units", [])
    for u in units:
        if u.get("device", "").lower() == device_name.lower():
            return JSONResponse(content=u)
    return JSONResponse(content={"error": "Device not found"}, status_code=404)

# endpoint "ask" — simple search dans la base
class AskIn(BaseModel):
    question: str

@app.post("/api/ask")
def ask(q: AskIn):
    q_lower = q.question.lower().strip()
    units = data.get("units", [])
    results = []
    for u in units:
        # champs recherchés (device, scenario, quick_checks, safety, common_causes)
        text_parts = []
        for key in ["device", "scenario", "quick_checks", "safety", "common_causes"]:
            val = u.get(key)
            if isinstance(val, list):
                text_parts.extend(val)
            elif val:
                text_parts.append(str(val))
        combined = " ".join([str(t).lower() for t in text_parts if t])
        if q_lower in combined:
            results.append({
                "device": u.get("device"),
                "scenario": u.get("scenario"),
                "quick_checks": u.get("quick_checks", []),
                "fixes": u.get("fixes", {})
            })
    if results:
        return {"answer": f"{len(results)} résultat(s) trouvé(s).", "results": results}
    return {"answer": f"Désolé, je n'ai rien trouvé pour «{q.question}»."}
