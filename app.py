from flask import Flask, jsonify
import json

app = Flask(__name__)

# Charger les données depuis ton fichier JSON
with open("data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Route principale
@app.route("/")
def index():
    return "Robot Christophe Actif"

# Route pour afficher les données
@app.route("/items")
def get_items():
    return jsonify(data)
from flask import request

# Route pour rechercher les données
@app.route("/items/search")
def search_items():
    categorie = request.args.get("categorie")  # lit ?categorie=X dans l'URL
    if not categorie:
        return jsonify({"error": "Veuillez fournir une catégorie"}), 400

    result = [item for item in data if item.get("categorie") == categorie]
    return jsonify(result)


if __name__ == "__main__":
    # Lancer le serveur Flask en local
    app.run(host="0.0.0.0", port=5000, debug=True)
