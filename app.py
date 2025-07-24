from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

# ✅ Charge l’index JSON des PLU au démarrage
with open("index_plu_4departements.json", "r", encoding="utf-8") as f:
    index_plu = json.load(f)

@app.route("/get-plu", methods=["POST"])
def get_plu():
    data = request.get_json()
    adresse = data.get("adresse")

    if not adresse:
        return jsonify({"error": "Aucune adresse fournie"}), 400

    # ✅ Appel à l’API OpenCage pour obtenir la commune
    api_key = "b71bdf9bdf5045e7bd4d915b79189721"
    geo_url = f"https://api.opencagedata.com/geocode/v1/json?q={adresse}&key={api_key}&language=fr&pretty=1"
    geo_response = requests.get(geo_url)
    geo_data = geo_response.json()

    # 🔍 Pour debug : affiche les données brutes de OpenCage (visible dans Render)
    print(json.dumps(geo_data, indent=2, ensure_ascii=False))

    try:
        components = geo_data["results"][0]["components"]
        commune = (
            components.get("city") or
            components.get("town") or
            components.get("village") or
            components.get("municipality")
        )

        if not commune:
            return jsonify({'error': 'Commune introuvable dans les données OpenCage'}), 404

        commune = commune.strip().title()

    except Exception as e:
        return jsonify({'error': f'Erreur lors du traitement OpenCage: {str(e)}'}), 500

    # 🔍 Cherche la commune dans l’index PLU
    if commune in index_plu:
        info = index_plu[commune]
        return jsonify({
            "commune": commune,
            "code_insee": info["code_insee"],
            "lien_pdf": info["pdf"]
        })
    else:
        return jsonify({"error": f"La commune « {commune} » n'est pas dans l’index PLU"}), 404

@app.route("/", methods=["GET"])
def home():
    return "API GPT-Ease PLU en ligne 🚀", 200
)
