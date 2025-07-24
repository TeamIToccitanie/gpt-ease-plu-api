import json
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/get-plu", methods=["POST"])
def get_plu():
    # Lecture de l'adresse envoyée
    data = request.get_json()
    adresse = data.get("adresse")

    if not adresse:
        return jsonify({"error": "Adresse manquante"}), 400

    # Requête à l'API OpenCage
    url_geo = f"https://api.opencagedata.com/geocode/v1/json?q={adresse}&key=b71bdf9bdf9545e7bd4d915b79189721"
    try:
        geo_response = requests.get(url_geo)
        geo_data = geo_response.json()
    except Exception as e:
        return jsonify({"error": f"Erreur lors de la requête OpenCage : {str(e)}"}), 500

    # Extraction de la commune
    try:
        components = geo_data["results"][0]["components"]
        commune = (
            components.get("city") or
            components.get("town") or
            components.get("village") or
            components.get("municipality")
        )
    except (KeyError, IndexError):
        return jsonify({"error": "Impossible de lire les données OpenCage"}), 500

    if not commune:
        return jsonify({"error": "Commune introuvable dans les données OpenCage"}), 404

    # Normalisation de la commune
    commune = commune.strip().title()

    # Lecture du fichier d’index JSON
    try:
        with open("index_plu_4departements.json", "r", encoding="utf-8") as f:
            index_data = json.load(f)
    except Exception as e:
        return jsonify({"error": f"Erreur de lecture du fichier index : {str(e)}"}), 500

    # Recherche du PDF
    pdf_url = index_data.get(commune, {}).get("pdf")

    if not pdf_url:
        return jsonify({"error": "PLU non trouvé pour cette commune"}), 404

    return jsonify({
        "commune": commune,
        "pdf_url": pdf_url
    })

# Lancement local
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

pdf_url = index_data.get(commune, {}).get("pdf")

    if not pdf_url:
        return jsonify({"error": "PLU non trouvé pour cette commune"}), 404

    return jsonify({"commune": commune, "pdf_url": pdf_url})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
