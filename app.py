import json
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/get-plu", methods=["POST"])
def get_plu():
    data = request.get_json()
    adresse = data.get("adresse")

    if not adresse:
        return jsonify({"error": "Adresse manquante"}), 400

    # Requête vers l’API OpenCage pour géocoder l’adresse
    url_geo = f"https://api.opencagedata.com/geocode/v1/json?q={adresse}&key=b71bdf9bdf5045e7bd4d915b79189721"
    geo_response = requests.get(url_geo)
    geo_data = geo_response.json()

    # 🎯 Étape 1 : Affiche les données brutes (debug)
    print(json.dumps(geo_data, indent=2, ensure_ascii=False))

    # 🎯 Étape 2 : Récupération sécurisée de la commune
    try:
        components = geo_data["results"][0]["components"]
        commune = (
            components.get("city")
            or components.get("town")
            or components.get("village")
            or components.get("municipality")
        )
    except (KeyError, IndexError):
        return jsonify({"error": "Impossible de lire les données OpenCage"}), 500

    if not commune:
        return jsonify({"error": "Commune introuvable dans les données OpenCage"}), 404

    # 🎯 Étape 3 : Normalise le nom de commune
    commune = commune.strip().title()

    # Lecture du fichier index
with open("index_plu_4departements.json", "r", encoding="utf-8") as f:
    index_data = json.load(f)

pdf_url = index_data.get(commune, {}).get("pdf")

    if not pdf_url:
        return jsonify({"error": "PLU non trouvé pour cette commune"}), 404

    return jsonify({"commune": commune, "pdf_url": pdf_url})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
