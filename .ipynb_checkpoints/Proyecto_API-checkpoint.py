import requests
import json

API_KEY = '1a9ea75b5f92dfda381d817fc00e5458' 
USER_AGENT = '808e0a8bbaf9d30bf181edb60c742824'  

headers = {
    'user-agent': USER_AGENT
}

##sacar top artists
params = {
    'method': 'chart.getTopArtists',
    'api_key': API_KEY,
    'format': 'json'
}

response = requests.get('https://ws.audioscrobbler.com/2.0/', headers=headers, params=params)

if response.status_code == 200:
    data = response.json()
else:
    print(f"Error en la solicitud: {response.status_code}")


##sacar top artistas por pais

COUNTRY = 'Spain' 
LIMIT = 10  ##Número de resultados a obtener

url = 'https://ws.audioscrobbler.com/2.0/'
params = {
    'method': 'geo.getTopArtists',
    'country': COUNTRY,
    'api_key': API_KEY,
    'format': 'json',
    'limit': LIMIT
}

response = requests.get(url, params=params)
data = response.json()