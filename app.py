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
    return "API active. Allez sur /chatpage pour tester le chat."

# ✅ Page de chat web
@app.route("/chatpage")
def chatpage():
    return render_template("chat.html")  # ton chat.html avec le CSS vert pastel / fond bleu

# ✅ Endpoint API
@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        if not data or "message" not in data:
            return jsonify({"answer": "⚠️ Envoie un message valide."})

        user_message = data["message"]

        # Recherche dans la base JSON
        kb_entry = search_in_kb(user_message)

        # Construction du prompt pour OpenAI
        messages = [
            {"role": "system", "content": "Tu es un assistant technique qui aide à diagnostiquer des pannes d’appareils électroménagers en utilisant une base JSON."},
            {"role": "user", "content": user_message}
        ]

        if kb_entry:
            context = f"Voici des infos issues de la base : {json.dumps(kb_entry, ensure_ascii=False)}"
            messages.append({"role": "system", "content": context})

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
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
