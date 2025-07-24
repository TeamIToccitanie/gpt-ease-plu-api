import requests
import json

# Étape 1 – Récupérer toutes les communes de Haute-Savoie (département 74)
url = "https://geo.api.gouv.fr/departements/74/communes?fields=nom&format=json"
response = requests.get(url)
communes = response.json()

# Étape 2 – Créer le JSON avec PDF fictif à compléter ensuite
index = {}
for commune in communes:
    nom = commune['nom']
    index[nom] = {
        "pdf": f"https://drive.google.com/file/d/ID_{nom.replace(' ', '_')}/view?usp=sharing"
    }

# Étape 3 – Sauvegarde locale du fichier
with open("index_haute_savoie.json", "w", encoding="utf-8") as f:
    json.dump(index, f, ensure_ascii=False, indent=2)

print("✅ Fichier index_haute_savoie.json généré avec succès.")
