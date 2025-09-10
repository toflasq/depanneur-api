from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)  # Autorise les requêtes depuis n'importe quel domaine (utile pour Render)

# Charger ton JSON
with open("data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Route racine
@app.route("/")
def index():
    return "Robot Christophe Actif"

# Route pour toutes les données
@app.route("/items")
def get_items():
    return jsonify(data)

# Route recherche par catégorie
@app.route("/items/search")
def search_items():
    categorie = request.args.get("categorie")
    if not categorie:
        return jsonify({"error": "Veuillez fournir une catégorie"}), 400
    result = [item for item in data if item.get("categorie") == categorie]
    return jsonify(result)

# Route recherche par nom
@app.route("/items/name")
def search_by_name():
    nom = request.args.get("nom")
    if not nom:
        return jsonify({"error": "Veuillez fournir un nom"}), 400
    result = [item for item in data if item.get("nom") == nom]
    return jsonify(result)

# Route recherche par ID
@app.route("/items/id")
def search_by_id():
    id_str = request.args.get("id")
    if not id_str:
        return jsonify({"error": "Veuillez fournir un id"}), 400
    try:
        id_int = int(id_str)
    except ValueError:
        return jsonify({"error": "ID doit être un nombre"}), 400
    result = [item for item in data if item.get("id") == id_int]
    return jsonify(result)

# Route chat pour API
@app.route("/chat")
def chat():
    user_msg = request.args.get("message")
    if not user_msg:
        return jsonify({"reply": "Envoyez un message valide."})
    # Pour l'instant, écho simple
    reply = f"Tu as dit : {user_msg}"
    return jsonify({"reply": reply})

# Route pour interface web du chat
@app.route("/chatpage")
def chatpage():
    return render_template("chat.html")  # chat.html doit être dans templates/

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
