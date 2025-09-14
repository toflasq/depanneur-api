# app.py
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from openai import OpenAI
import os
import json

app = Flask(__name__)
CORS(app)

# 🔑 Clé API OpenAI (à configurer dans Render → Environment Variables)
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
    return "API active. Accède à /chatpage pour utiliser le Robot Dépanneur Christophe."

# ✅ Page de chat web
@app.route("/chatpage")
def chatpage():
    return render_template("chat.html")

# ✅ Endpoint API
@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_message = request.json.get("message", "").strip()
        if not user_message:
            return jsonify({"answer": "Envoie une question valide."})

        kb_entry = search_in_kb(user_message)

        # Construction du prompt
        prompt = "Tu es un assistant technique qui aide à diagnostiquer des pannes d’appareils électroménagers. "
        if kb_entry:
            prompt += f"Voici des infos issues de la base de données : {json.dumps(kb_entry, ensure_ascii=False)}. "
        prompt += f"Réponds clairement à la question suivante : {user_message}"

        messages = [{"role": "user", "content": prompt}]

        # Appel OpenAI
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )
        reply = response.choices[0].message.content

        return jsonify({"answer": reply})

    except Exception as e:
        return jsonify({"answer": f"⚠️ Erreur serveur : {str(e)}"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
