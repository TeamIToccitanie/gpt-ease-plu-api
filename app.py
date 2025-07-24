from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/api/plu', methods=['GET'])
def get_plu():
    adresse = request.args.get('adresse')
    if not adresse:
        return jsonify({'error': 'Paramètre "adresse" requis'}), 400

    # 🔍 Géocodage avec OpenCage
    opencage_api_key = 'b71bdf9bdf954e57bd4d915b79189721'
    geo_url = f"https://api.opencagedata.com/geocode/v1/json?q={adresse}&key={opencage_api_key}"
    geo_response = requests.get(geo_url)
    geo_data = geo_response.json()

    try:
        coords = geo_data['results'][0]['geometry']
        lat, lng = coords['lat'], coords['lng']
    except (KeyError, IndexError):
        return jsonify({'error': 'Adresse introuvable'}), 404

    # 🗺️ Appel API PLU Géoportail
    plu_url = f"https://www.geoportail-urbanisme.gouv.fr/api/urbanisme/zone/commune?lat={lat}&lon={lng}"
    plu_response = requests.get(plu_url)
    if plu_response.status_code != 200:
        return jsonify({'error': 'Erreur lors de l’appel à l’API PLU'}), 500
    plu_data = plu_response.json()

    # ✅ Retour complet
    return jsonify({
        'adresse': adresse,
        'lat': lat,
        'lng': lng,
        'plu': plu_data
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
