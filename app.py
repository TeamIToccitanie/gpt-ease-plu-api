from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

# Chargement de l’index JSON
with open("index_plu_4departements.json", "r", encoding="utf-8") as f:
    index_pdf = json.load(f)

@app.route('/api/plu', methods=['GET'])
def get_plu():
    adresse = request.args.get('adresse')
    if not adresse:
        return jsonify({'error': 'Paramètre "adresse" requis'}), 400

    # 🔍 Géocodage via OpenCage
    opencage_api_key = 'b71bdf9bdf954e57bd4d915b79189721'
    geo_url = f"https://api.opencagedata.com/geocode/v1/json?q={adresse}&key={opencage_api_key}"
    geo_response = requests.get(geo_url)
    geo_data = geo_response.json()

    try:
        components = geo_data['results'][0]['components']
        commune = (
    components.get('city') or
    components.get('town') or
    components.get('village') or
    components.get('city_district')
)
        if not commune:
            return jsonify({'error': 'Commune non trouvée'}), 404
    except (KeyError, IndexError):
        return jsonify({'error': 'Adresse introuvable'}), 404

    # 🔗 Recherche du lien PDF
    lien_pdf = index_pdf.get(commune)
    if not lien_pdf:
        return jsonify({
            'commune': commune,
            'pdf': None,
            'message': f"Aucun PDF trouvé pour la commune : {commune}"
        }), 404

    return jsonify({
        'commune': commune,
        'pdf': lien_pdf,
        'message': f"PDF trouvé pour la commune : {commune}"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
