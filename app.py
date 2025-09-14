from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from openai import OpenAI
import os
import json

app = Flask(__name__)
CORS(app)

# 🔑 Clé API OpenAI (configurée dans Render → Environment Variables)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 📂 Charger la base JSON
with open("data.json", "r", encoding="utf-8") as f:
    knowledge_base = json.load(f)

# 🔍 Recherche simple dans la base
def search_in_kb(user_message):
    user_message = user_message.lower()
    for item in knowledge_base:
        if item["device"].lower() in user_message and item["scenario"].lower() in user_message:
            return item
    return None

# ✅ Page d’accueil
@app.route("/")
def index():
    return "API active. Allez sur /chatpage pour tester l'interface."

# ✅ Page de chat web
@app.route("/chatpage")
def chatpage():
    return render_template("chat.html")

# ✅ Endpoint API
@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")
    if not user_message:
        return jsonify({"answer": "Envoie une question valide."})

    kb_entry = search_in_kb(user_message)

    messages = [
        {"role": "system", "content": "Tu es un assistant technique qui aide à diagnostiquer des pannes d’appareils électroménagers en utilisant une base JSON."},
        {"role": "user", "content": user_message}
    ]

    if kb_entry:
        context = f"Voici des infos issues de la base de données : {json.dumps(kb_entry, ensure_ascii=False)}"
        messages.append({"role": "system", "content": context})

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )
        reply = response.choices[0].message.content
    except Exception as e:
        reply = f"Erreur GPT: {str(e)}"

    return jsonify({"answer": reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

