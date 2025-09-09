from fastapi import FastAPI
from fastapi.responses import JSONResponse
import json, os

app = FastAPI(title="Dépanneur API")
DATA_FILE = os.path.join(os.path.dirname(__file__), "data.json")
with open(DATA_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

@app.get("/")
def root():
    return {"message": "Bienvenue sur le Web Service Dépanneur!"}

@app.get("/devices")
def list_devices():
    units = data.get("units", [])
    devices = [{"category": u.get("category"), "device": u.get("device")} for u in units]
    return JSONResponse(content=devices)

@app.get("/device/{device_name}")
def get_device(device_name: str):
    units = data.get("units", [])
    for u in units:
        if u.get("device").lower() == device_name.lower():
            return JSONResponse(content=u)
    return JSONResponse(content={"error": "Device not found"}, status_code=404)

@app.get("/modules")
def list_modules():
    return JSONResponse(content=data.get("modules", []))
