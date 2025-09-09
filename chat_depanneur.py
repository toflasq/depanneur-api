import json

# Charger le fichier JSON
with open("data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

def afficher_devices():
    print("Appareils disponibles :")
    for i, unit in enumerate(data.get("units", []), 1):
        print(f"{i}. {unit['device']} ({unit['category']})")

def repondre_question(question):
    question = question.lower()
    for unit in data.get("units", []):
        device = unit["device"].lower()
        if device in question:
            scenario = unit.get("scenario", "Scénario inconnu")
            safety = "\n".join(unit.get("safety", []))
            steps = " | ".join([step["action"] for step in unit.get("diagnostic_flow", [])])
            response = f"Appareil: {unit['device']}\nScénario: {scenario}\nSécurité:\n{safety}\nÉtapes diagnostiques: {steps}"
            return response
    return "Désolé, je n'ai pas trouvé d'infos pour cet appareil."

def main():
    print("Bienvenue dans le Chat Dépanneur !")
    afficher_devices()
    while True:
        question = input("\nPose ta question (ou tape 'quit' pour sortir) : ")
        if question.lower() in ['quit', 'exit']:
            print("Fin du chat. Bye!")
            break
        réponse = repondre_question(question)
        print("\n" + réponse)

if __name__ == "__main__":
    main()
