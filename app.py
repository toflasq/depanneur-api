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
# Route  pour rechercher les objets
@app.route("/items/name")
def search_by_name():
    nom = request.args.get("nom")  # lit ?nom=Objet A
    if not nom:
        return jsonify({"error": "Veuillez fournir un nom"}), 400

    result = [item for item in data if item.get("nom") == nom]
    return jsonify(result)

# Route  pour rechercher les objets par id
@app.route("/items/id")
def search_by_id():
    id_str = request.args.get("id")  # lit ?id=2
    if not id_str:
        return jsonify({"error": "Veuillez fournir un id"}), 400

    try:
        id_int = int(id_str)
    except ValueError:
        return jsonify({"error": "ID doit être un nombre"}), 400

    result = [item for item in data if item.get("id") == id_int]
    return jsonify(result)



if __name__ == "__main__":
    # Lancer le serveur Flask en local
    app.run(host="0.0.0.0", port=5000, debug=True)
