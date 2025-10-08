

import sqlite3
import webbrowser
from playsound import playsound
from engine.config import ASSISTANT_NAME
import os
from engine.command import speak
import eel
import pywhatkit as kit
import re
from rapidfuzz import process
from engine.helper import extract_yt_term
import pvporcupine
import pyaudio
import struct
import time
from engine.helper import remove_words
from urllib.parse import quote
import subprocess
import pyautogui
from engine.spotify import sp
import spotipy
from spotipy.oauth2 import SpotifyOAuth


con = sqlite3.connect('sexta-feira.db')


cursor = con.cursor()




@eel.expose 
def playAssistantSound():
	music_dir = r"C:\Users\Rouue\Desktop\jarvis\www\assets\audio\zapsplat_multimedia_beep_high_tech_with_reverb_007_87543.mp3"
	playsound(music_dir)

def openCommand(query):
    # Normaliza
    query = query.lower()
    query = query.replace(ASSISTANT_NAME.lower(), "")
    query = query.replace("abrir", "")
    query = query.strip()

    # Remove palavras irrelevantes (stopwords)
    stopwords = ["o", "no", "na", "a", "um", "uma", "os", "as", "de", "do", "da"]
    tokens = [t for t in query.split() if t not in stopwords]
    app_name = " ".join(tokens)

    if not app_name:
        speak("não entendi o que você quer abrir")
        return

    try:
        # 1 - Busca direta no banco (LIKE)
        cursor.execute("SELECT path FROM sys_command WHERE name LIKE ?", (f"%{app_name}%",))
        results = cursor.fetchall()
        if results:
            speak(f"abrindo {app_name}")
            os.startfile(results[0][0])
            return

        # 2 - Busca site no banco (LIKE)
        cursor.execute("SELECT url FROM web_command WHERE name LIKE ?", (f"%{app_name}%",))
        results = cursor.fetchall()
        if results:
            speak(f"abrindo {app_name}")
            webbrowser.open(results[0][0])
            return

        # 3 - Fuzzy matching em programas (se LIKE não achar nada)
        cursor.execute("SELECT name, path FROM sys_command")
        apps = cursor.fetchall()
        if apps:
            best_match = process.extractOne(app_name, [a[0] for a in apps])
            if best_match and best_match[1] > 80:  # 80% de similaridade
                index = [a[0] for a in apps].index(best_match[0])
                path = apps[index][1]
                speak(f"abrindo {best_match[0]}")
                os.startfile(path)
                return
            

		# 4  - fuzzy matching em sites (se LIKE não achar nada)
        cursor.execute("SELECT name, url FROM web_command")
        sites = cursor.fetchall()
        if sites:
            best_match = process.extractOne(app_name, [s[0] for s in sites])
            if best_match and best_match[1] > 80:  # 80% de similaridade
                index = [s[0] for s in sites].index(best_match[0])
                url = sites[index][1]
                speak(f"abrindo {best_match[0]}")
                webbrowser.open(url)
                return

        # 5 - Última tentativa: abrir pelo Windows
        speak(f"abrindo {app_name}")
        os.system(f'start {app_name}')

    except Exception as e:
        speak("algo deu errado")
        print("Erro:", e)

def PlayYoutube(query):
    search_term = extract_yt_term(query)
    speak("Reproduzindo "+search_term+" no YouTube")
    kit.playonyt(search_term)




# hot word detection

def hotword():
    porcupine=None
    paud=None
    audio_stream=None
    try:
       
        # pre trained keywords    
        porcupine=pvporcupine.create(keywords=["alexa"])
        paud=pyaudio.PyAudio()
        audio_stream=paud.open(rate=porcupine.sample_rate,channels=1,format=pyaudio.paInt16,input=True,frames_per_buffer=porcupine.frame_length)
        
        # loop for streaming
        while True:
            keyword=audio_stream.read(porcupine.frame_length)
            keyword=struct.unpack_from("h"*porcupine.frame_length,keyword)

            # processing keyword comes from mic 
            keyword_index=porcupine.process(keyword)

            # checking first keyword detetcted for not
            if keyword_index>=0:
                print("hotword detected")

                # pressing shorcut key win+j
                import pyautogui as autogui
                autogui.keyDown("win")
                autogui.press("j")
                time.sleep(2)
                autogui.keyUp("win")
                 
    
                
    except:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()


# find contacts
def findContact(query):
    print("Query antes da limpeza:", query)
    words_to_remove = [
    ASSISTANT_NAME,
    'ligar', 'telefonar', 'chamar', 'falar',
    'mandar', 'enviar',
    'mensagem', 'áudio', 'vídeo',
    'zap', 'whatsapp', 'sms',
    'para', 'pro', 'a', 'o',' no', 'um', 'uma', 'de','para o','pra'
]
    query = remove_words(query, words_to_remove)
    print("Query final após limpeza:", query)

    try:
        query = query.strip().lower()
        cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
        results = cursor.fetchall()
        print(results[0][0])
        mobile_number_str = str(results[0][0])

        if not mobile_number_str.startswith('+55'):
            mobile_number_str = '+55' + mobile_number_str

        return mobile_number_str, query
    except:
        speak('not exist in contacts')
        print(query, results)
        return 0, 0
    



def whatsApp(mobile_no, message, flag, name):
    

    if flag == 'mensagem':
        target_tab = 12
        jarvis_message = "mensagem enviada com sucesso "+name

    elif flag == 'ligar':
        target_tab = 7
        message = ''
        jarvis_message = "ligando para "+name

    else:
        target_tab = 6
        message = ''
        jarvis_message = "iniciando chamada de video "+name


    # Encode the message for URL
    encoded_message = quote(message)
    print(encoded_message)
    # Construct the URL
    whatsapp_url = f"whatsapp://send?phone={mobile_no}&text={encoded_message}"

    # Construct the full command
    full_command = f'start "" "{whatsapp_url}"'

    # Open WhatsApp with the constructed URL using cmd.exe
    subprocess.run(full_command, shell=True)
    time.sleep(5)
    subprocess.run(full_command, shell=True)
    
    pyautogui.hotkey('ctrl', 'f')

    for i in range(1, target_tab):
        pyautogui.hotkey('tab')

    pyautogui.hotkey('enter')
    speak(jarvis_message)



##play musica no spotify

def playSpotify(query):
    subprocess.run('start spotify:', shell=True)
    time.sleep(5)  # espera o app abrir

    devices = sp.devices()['devices']
    if not devices:
        print("Nenhum dispositivo ativo encontrado")
        return

    # Filtra apenas dispositivos que estão ativos
    active_devices = [d for d in devices if d['is_active']]
    if active_devices:
        devices_id = active_devices[0]['id']
    else:
        # Se nenhum estiver ativo, usa o primeiro disponível
        devices_id = devices[0]['id']

    print("Usando device_id:", devices_id)

    ##logica para pesquisar no device di e tocar musica

    # Opcional: remover palavras comuns tipo "tocar", "no Spotify", "play"
    words_to_remove = ["tocar", "play", "no spotify", "spotify"]
    for word in words_to_remove:
        query = query.lower().replace(word, "").strip()
    print("Nome da música após limpeza:", query)

    ##pesquisar musica no spotify
    results = sp.search(q=query, type="track", limit=1)
    if results['tracks']['items']:
        track_uri = results['tracks']['items'][0]['uri']
        track_name = results['tracks']['items'][0]['name']
        track_artist = results['tracks']['items'][0]['artists'][0]['name']
 

    else:
        print("Música não encontrada no Spotify")
        return

    try:
        sp.start_playback(device_id=devices_id, uris=[track_uri])
        print(f"Tocando: {track_name} - {track_artist}")
        speak("Tocando: " + track_name + " - " + track_artist + " no Spotify")
    except spotipy.SpotifyException as e:
        print("Erro ao tentar reproduzir:", e)



