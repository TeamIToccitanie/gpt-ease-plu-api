from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/api/plu', methods=['GET'])
def get_plu():
    adresse = request.args.get('adresse')
    if not adresse:
        return jsonify({'error': 'Paramètre "adresse" requis'}), 400

    # Étape 1 : géocodage avec OpenCage
    opencage_api_key = 'b71bdf9bdf5045e7bd4d915b79189721'
    url = "https://api.opencagedata.com/geocode/v1/json?q=" + adresse + "&key=" + opencage_api_key
    response = requests.get(url)
    data = response.json()

    try:
        coords = data['results'][0]['geometry']
        lat, lng = coords['lat'], coords['lng']
    except (KeyError, IndexError):
        return jsonify({'error': 'Adresse introuvable'}), 404

    # Étape 2 : retour JSON simple pour test
    return jsonify({'adresse': adresse, 'lat': lat, 'lng': lng})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)



