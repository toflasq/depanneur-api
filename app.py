from flask import Flask, jsonify, request, render_template
import json

app = Flask(__name__)

# Charger ton JSON
with open("data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

@app.route("/")
def index():
    return "Robot Christophe Actif"

@app.route("/items")
def get_items():
    return jsonify(data)

# Route chat simple
@app.route("/chat")
def chat():
    user_msg = request.args.get("message")
    reply = f"Tu as dit : {user_msg}"  # pour tester, plus tard on mettra GPT ici
    return jsonify({"reply": reply})

# Route pour l'interface chat
@app.route("/chatpage")
def chatpage():
    return render_template("chat.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
