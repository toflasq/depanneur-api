from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from openai import OpenAI
import os
import json

app = Flask(__name__)
CORS(app)

# 🔑 Charge ta clé API OpenAI depuis les variables d'environnement Render
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
if os.getenv("OPENAI_API_KEY") is None:
    print("⚠️ OPENAI_API_KEY manquante !")

# 📂 Charger ton JSON
with open("data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# ✅ Route racine
@app.route("/")
def index():
    return "Robot Christophe Actif"

# ✅ Route pour interface chat web
@app.route("/chatpage")
def chatpage():
    return render_template("chat.html")

# ✅ Route Chat (fusion Data.json + GPT)
@app.route("/chat")
def chat():
    user_msg = request.args.get("message")
    context = f"L'utilisateur a demandé : {user_msg}"
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Tu es Robot Christophe, assistant."},
                {"role": "user", "content": context}
            ]
        )
        reply = response.choices[0].message.content
    except Exception as e:
        reply = f"Erreur GPT: {str(e)}"
    
    return jsonify({"reply": reply})


    # 🔍 Chercher dans data.json
    results = []
    for item in data:
        if user_msg.lower() in str(item.get("nom", "")).lower():
            results.append(item)
        elif user_msg.lower() in str(item.get("categorie", "")).lower():
            results.append(item)
        elif user_msg.isdigit() and int(user_msg) == item.get("id"):
            results.append(item)

    # Construit le contexte
    context = f"L'utilisateur a demandé : {user_msg}\n"
    if results:
        context += f"Données trouvées dans data.json : {results}\n"
    else:
        context += "Aucune donnée directe trouvée dans data.json.\n"

    # 💬 Appel GPT-4o mini
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Tu es Robot Christophe, un assistant qui combine données JSON et intelligence GPT."},
                {"role": "user", "content": context}
            ]
        )
        reply = response.choices[0].message.content
    except Exception as e:
        reply = f"Erreur GPT: {str(e)}"

    return jsonify({"reply": reply})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)



