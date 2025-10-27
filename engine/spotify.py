import subprocess
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth

from engine.command import speak




##autenticação spotify
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id="8182aa2d20cf45c0996443b88d5525bf",
    client_secret="d8eb2b85ea7c41679643890e63ec2db1",
    redirect_uri="http://127.0.0.1:8888/callback",
    scope="user-read-playback-state user-modify-playback-state user-read-currently-playing"
))



## play em musica no spotify
def playSpotify(song=None, artist=None):
     
    subprocess.run('start spotify:', shell=True)
    time.sleep(5)

    devices = sp.devices().get('devices', [])
    if not devices:
        print("Nenhum dispositivo ativo encontrado")
        return

    active_devices = [d for d in devices if d['is_active']]
    device_id = active_devices[0]['id'] if active_devices else devices[0]['id']
    print("Usando device_id:", device_id)

    # 🔍 MELHORIA 1 — Busca mais específica se tiver artista
    
    search_query = song
    if artist:
        search_query += f" artist:{artist}"
            
    
    
    print("Buscando no Spotify:", search_query)

    # 🔍 MELHORIA 2 — Aumenta o limite para verificar mais resultados
    results = sp.search(q=search_query, type="track", market="BR", limit=5)

    if not results['tracks']['items']:
        print("Música não encontrada. Tentando busca mais ampla...")
        results = sp.search(q=song, type="track", market="BR", limit=5)

    # 🔍 MELHORIA 3 — Pega a primeira que realmente bate com o nome e artista
    track = None
    for item in results['tracks']['items']:
        name_match = song.lower() in item['name'].lower()
        artist_match = artist and artist.lower() in item['artists'][0]['name'].lower()
        if name_match and (not artist or artist_match):
            track = item
            break

    if not track:
        print("Nenhum resultado relevante encontrado.")
        speak("Não encontrei essa música no Spotify.")
        return

    track_uri = track['uri']
    track_name = track['name']
    track_artist = track['artists'][0]['name']

    try:
        sp.start_playback(device_id=device_id, uris=[track_uri])
        print(f"Tocando: {track_name} - {track_artist}")
        speak(f"Tocando {track_name} de {track_artist} no Spotify.")
    except spotipy.SpotifyException as e:
        print("Erro ao tentar reproduzir:", e)



##funcionalidade pausar musica no spotify
def pauseSpotify():
    devices = sp.devices().get('devices', [])
    
    if not devices:
        print("Nenhum dispositivo disponível no Spotify")
        speak("Nenhum dispositivo disponível no Spotify")
        return
    
    # pega o primeiro device ativo, ou o primeiro da lista se nenhum estiver ativo
    active_device = next((d for d in devices if d['is_active']), devices[0])
    device_id = active_device['id']
    
    try:
        sp.pause_playback(device_id=device_id)
        print("Música pausada no Spotify")
        speak("Seu Spotify foi pausado")
    except Exception as e:
        print("Erro ao pausar a música:", e)
        speak("Não consegui pausar a música no Spotify")


##funcionalidade resume musica no spotify
def resumeSpotify():
    devices = sp.devices().get('devices', [])
    
    if not devices:
        print("Nenhum dispositivo disponível no Spotify")
        speak("Nenhum dispositivo disponível no Spotify")
        return
    
    # pega o primeiro device ativo
    active_device = next((d for d in devices if d['is_active']), devices[0])
    device_id = active_device['id']
    
    try:
        speak("Retomando sua música no Spotify")
        sp.start_playback(device_id=device_id)
        print("Música retomada no Spotify")
        
    except Exception as e:
        print("Erro ao retomar a música:", e)
        speak("Não consegui retomar a música no Spotify")

##funcionalidade next musica no spotify
def next_track():
    devices = sp.devices().get('devices', [])
    
    if not devices:
        print("Nenhum dispositivo disponível no Spotify")
        speak("Nenhum dispositivo disponível no Spotify")
        return
    
    # pega o primeiro device ativo, ou o primeiro da lista se nenhum estiver ativo
    active_device = next((d for d in devices if d['is_active']), devices[0])
    device_id = active_device['id']
    
    try:
        sp.next_track(device_id=device_id)
        print("Próxima música")
        speak("Tocando a próxima música")
    except Exception as e:
        print("Erro ao avançar a música:", e)
        speak("Não consegui avançar para a próxima música")

##funcionalidade previous musica no spotify
def previous_track():
    devices = sp.devices().get('devices', [])
    
    if not devices:
        print("Nenhum dispositivo disponível no Spotify")
        speak("Nenhum dispositivo disponível no Spotify")
        return
    
    # pega o primeiro device ativo, ou o primeiro da lista se nenhum estiver ativo
    active_device = next((d for d in devices if d['is_active']), devices[0])
    device_id = active_device['id']
    
    try:
        sp.previous_track(device_id=device_id)
        print("Música anterior")
        speak("Voltando para a música anterior")
    except Exception as e:
        print("Erro ao voltar a música:", e)
        speak("Não consegui voltar para a música anterior")

###comando para toca playlist no spotify
def play_playlist(query):
    
    # 🎶 Mapeamento de playlists específicas
    playlists = {
        "treino": "spotify:playlist:1FYxAHHjbip2ljXrBPlBoW",
        "minha": "spotify:playlist:27YA2q5pKK7qP3PSc5lGrG",  # URI em vez de link
        "romântica":"spotify:playlist:35iWnJZZjSp91lSfjbRmsQ",
        "pagode" : "spotify:playlist:5WBhPjQLT8tyoz9YoFKxF2",
    }

    # 🚀 Abre o Spotify
    subprocess.run('start spotify:', shell=True)
    time.sleep(5)  # Espera o app abrir

    # 📱 Obtém os dispositivos
    devices = sp.devices()['devices']
    if not devices:
        print("Nenhum dispositivo ativo encontrado")
        return

    # 🔍 Seleciona o dispositivo ativo (ou o primeiro)
    active_devices = [d for d in devices if d['is_active']]
    if active_devices:
        devices_id = active_devices[0]['id']
    else:
        devices_id = devices[0]['id']

    print("Usando device_id:", devices_id)

    # 🧹 Limpa o texto do comando
    words_to_remove = ["tocar", "no spotify", "spotify", "playlist", "playlists"]
    for word in words_to_remove:
        query = query.lower().replace(word, "").strip()
    print("Nome da playlist após limpeza:", query)

    # 🎯 Verifica se o nome da playlist está no dicionário personalizado
    if query in playlists:
        playlist_uri = playlists[query]
        playlist_name = query
        playlist_owner = "Jeferson"
        print(f"🔊 Tocando playlist personalizada: {playlist_name}")
    else:
        # 🔎 Pesquisa no Spotify
        results = sp.search(q=query, type="playlist", limit=1)
        if results['playlists']['items']:
            playlist_uri = results['playlists']['items'][0]['uri']
            playlist_name = results['playlists']['items'][0]['name']
            playlist_owner = results['playlists']['items'][0]['owner']['display_name']
        else:
            print("Playlist não encontrada no Spotify")
            return

    # ▶️ Tenta reproduzir a playlist
    try:
        sp.start_playback(device_id=devices_id, context_uri=playlist_uri)
        print(f"Tocando playlist: {playlist_name} - {playlist_owner}")
        speak("Tocando a playlist " + playlist_name + " no Spotify")
    except spotipy.SpotifyException as e:
        print("Erro ao tentar reproduzir a playlist:", e)


def setSpotifyVolume(volume_percent):
    print(volume_percent)
    devices = sp.devices().get('devices', [])
    
    if not devices:
        print("Nenhum dispositivo encontrado.")
        return


 ### pega o dispositivo ativo ou o primeiro da lista
    active_device = next((d for d in devices if d['is_active']), devices[0])
    device_id = active_device['id']

    ##garante que o volume esteja entre 0 e 100
    volume_percent = max(0, min(volume_percent, 100))

    try:
        sp.volume(volume_percent, device_id=device_id)
        speak(f"Volume definido para {volume_percent} por cento no Spotify.")
        print(f"Volume definido para {volume_percent}% no dispositivo {active_device['name']}")
    except spotipy.SpotifyException as e:
        speak("Não consegui ajustar o volume no Spotify.")
        print("Erro ao ajustar volume:", e)
