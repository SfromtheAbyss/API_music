import requests
import base64
import pprint

CLIENT_ID = '563f9007f27c45eeabb30b4c9518f4a3'
CLIENT_SECRET = '95152fd2177a4a7e91a6fd179b9283ab'

##obtener token
def get_access_token():
    credentials = f"{CLIENT_ID}:{CLIENT_SECRET}"
    credentials_b64 = base64.b64encode(credentials.encode()).decode()

    headers = {
        'Authorization': f'Basic {credentials_b64}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {'grant_type': 'client_credentials'}

    response = requests.post('https://accounts.spotify.com/api/token', headers=headers, data=data)
    if response.status_code == 200:
        return response.json()['access_token']
    else:
        print(f"Error al obtener el token: {response.status_code}")
        print(response.json())
        return None
    
##Buscar artista
def get_artist_info(artist_name):
    access_token = get_access_token()
    if not access_token:
        return None

    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    params = {
        'q': artist_name,
        'type': 'artist',
        'limit': 1
    }

    response = requests.get('https://api.spotify.com/v1/search', headers=headers, params=params)
    if response.status_code == 200:
        results = response.json()
        items = results.get('artists', {}).get('items', [])
        if items:
            artist = items[0]
            artist_info = {
                'Nombre': artist['name'],
                'ID': artist['id'],
                'Géneros': artist.get('genres', []),
                'Popularidad': artist.get('popularity'),
                'Seguidores': artist.get('followers', {}).get('total'),
                'Enlace': artist['external_urls']['spotify'],
                'Imagen': artist['images'][0]['url'] if artist.get('images') else None
            }
            return pprint.pprint(artist_info)
        else:
            print("Artista no encontrado.")
            return None
    else:
        print(f"Error en la búsqueda: {response.status_code}")
        return None

    
##Buscar cancion
def search_track(track_name, artist_name=None):
    access_token = get_access_token()
    if not access_token:
        return None

    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    query = f'track:{track_name}'
    if artist_name:
        query += f' artist:{artist_name}'

    params = {
        'q': query,
        'type': 'track',
        'limit': 1
    }

    response = requests.get('https://api.spotify.com/v1/search', headers=headers, params=params)
    if response.status_code == 200:
        results = response.json()
        if results['tracks']['items']:
            track = results['tracks']['items'][0]
            track_info = {
                'ID': track['id'],
                'Nombre': track['name'],
                'Artista': track['artists'][0]['name'],
                'Popularidad': track['popularity'],
                'Duración (ms)': track['duration_ms'],
                'Número de pista': track['track_number'],
                'Disco': track['disc_number'],
                'Explícita': track['explicit'],
                'Enlace': track['external_urls']['spotify'],
                'Vista previa': track['preview_url'],
                'Mercados disponibles': track['available_markets'],
                'Álbum': {
                    'Nombre': track['album']['name'],
                    'Tipo': track['album']['album_type'],
                    'Fecha de lanzamiento': track['album']['release_date'],
                    'Número de pistas': track['album']['total_tracks'],
                    'Enlace': track['album']['external_urls']['spotify']
                }
            }
            return pprint.pprint(track_info)
        else:
            print("Canción no encontrada.")
            return None
    else:
        print(f"Error en la búsqueda: {response.status_code}")
        return None

##Buscar Album
def search_album(album_name, artist_name=None):
    access_token = get_access_token()
    if not access_token:
        return None

    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    query = f'album:{album_name}'
    if artist_name:
        query += f' artist:{artist_name}'

    params = {
        'q': query,
        'type': 'album',
        'limit': 1
    }

    response = requests.get('https://api.spotify.com/v1/search', headers=headers, params=params)
    if response.status_code == 200:
        results = response.json()
        if results['albums']['items']:
            album = results['albums']['items'][0]
            album_info = {
                'ID': album['id'],
                'Nombre': album['name'],
                'Artistas': [artist['name'] for artist in album['artists']],
                'Fecha de Lanzamiento': album['release_date'],
                'Tipo de Álbum': album['album_type'],
                'URI': album['uri'],
                'Enlace en Spotify': album['external_urls']['spotify'],
                'Imagen de Portada': album['images'][0]['url'] if album.get('images') else None,
                'Mercados Disponibles': album['available_markets'],
                'Número de Canciones': album['total_tracks'],
            }
            return pprint.pprint(album_info)
        else:
            print("Álbum no encontrado.")
            return None
    else:
        print(f"Error en la búsqueda: {response.status_code}")
        return None

##Obtiene las canciones mas escuchadas en un pais de un artista
def get_artist_top_tracks(artist_id, market='ES'):
    access_token = get_access_token()
    if not access_token:
        return

    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    url = f'https://api.spotify.com/v1/artists/{artist_id}/top-tracks'
    params = {'market': market}

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        tracks = response.json()['tracks']
        for idx, track in enumerate(tracks, start=1):
            name = track['name']
            popularity = track['popularity']
            preview_url = track['preview_url']
            external_url = track['external_urls']['spotify']
            print(f"{idx}. {name} (Popularidad: {popularity})")
            print(f"   Enlace: {external_url}")
            if preview_url:
                print(f"   Vista previa: {preview_url}")
            print()
    else:
        print(f"Error al obtener las canciones: {response.status_code}")

get_artist_info("Lana del Rey")
get_artist_top_tracks("00FQb4jTyendYWaN8pK0wa")