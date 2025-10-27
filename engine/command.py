import pyttsx3
import speech_recognition as sr
import eel
import time
from engine.gemini import chat_with_gemini
import json






def speak(text):   
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)  # Change index to change voices. 0 for
    engine.setProperty('rate', 240)  # Speed percent (can go over 100)
    eel.DisplayMessage(text)
    engine.say(text)
    eel.receiverText(text)
    engine.runAndWait()

@eel.expose
def takeCommand():

    
    
    
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print('Listening...')
        eel.DisplayMessage('Listening...')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=0.2)

        try:
            # Tempo menor evita travamento se o usuário não falar
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
        except sr.WaitTimeoutError:
            print("Listening timed out while waiting for phrase to start.")
            eel.DisplayMessage("Listening timed out.")
            return ""

    try:
        print('Recognizing...')
        eel.DisplayMessage('Recognizing...')
        query = r.recognize_google(audio, language='pt-br')
        print(f'User said: {query}\n')
        eel.DisplayMessage(query)
        time.sleep(0.5)  # ⏳ reduzido pra resposta mais rápida
        return query

    except Exception as e:
        print("Could not recognize speech:", e)
        eel.DisplayMessage("Não entendi, tente novamente.")
        return ""
    


@eel.expose
def allCommands(message=1):
    
    from engine.features import findContact, whatsApp
    
    

    # 🔁 Captura o comando
    if message == 1:
        query = takeCommand()
        print(f"Usuário disse: {query}")
        eel.senderText(query)
    else:
        query = message
        eel.senderText(query)

    if not query:
        speak("Não ouvi nada, pode repetir?")
        eel.ShowHood()
        return

    try:
        comando_valido = False  # controla se algum comando foi executado
        
        # 🧭 Abrir programas ou sites
        if "sexta-feira" in query.lower() or "sexta" in query.lower() or "cesta" in query.lower():

            ##importações necessarias
            from engine.spotify import play_playlist, pauseSpotify, previous_track, next_track, resumeSpotify, playSpotify, setSpotifyVolume
            from engine.features import openCommand, PlayYoutube
            from engine.gemini import chat_with_gemini
            print("query :" + query)
            response_chat = chat_with_gemini(query)
            print("resposta do chat ", response_chat)
            data = json.loads(response_chat)
            print("dados apos a limpeza : ", data)

            action = data.get("action")
            params = data.get("parameters")
            
            print("action localizada : " + action)
            if action == "chat":
                text = params.get("text", "")
                print("oque é dito pela assistente : " +text)
                speak(text)

            # 💻 Abrir programas ou sites
            elif action == "abrir_programa":
                program = params.get("program", "")
                if program:
                    openCommand(program)
                else:
                    speak("Não consegui entender qual programa você quer abrir.")

            ## abrir lol
            elif action == "open_lol":
                print(action)
                program = "league of legends"
                openCommand(program)

            # 🎵 SPOTIFY
            elif action == "spotify_play":
                song = params.get("song", "")
                artist = params.get("artist", "")
                playlist = params.get("playlist", "")
                if playlist:
                    play_playlist(playlist)
                elif song:
                    playSpotify(song, artist)
                else:
                    speak("Não entendi qual música ou playlist você quer ouvir.")

            elif action == "spotify_pause":
                pauseSpotify()

            elif action == "spotify_next":
                next_track()

            elif action == "spotify_previous":
                previous_track()

            elif action == "spotify_resume":
                resumeSpotify()

            elif action == "spotify_volume":
                print(action)               
                volume = params.get("volume", "")
                volume_int = int(volume)
                setSpotifyVolume(volume_int)

                

            # ▶️ YouTube
            elif action == "youtube_play":
                query = params.get("query", "")
                if query:
                    PlayYoutube(query)
                else:
                    speak("Não entendi qual vídeo você quer assistir.")

            # 💬 WhatsApp
            elif action == "enviar_mensagem":
                contact_name = params.get("contact_name", "")
                message_text = params.get("message", "")
                contact_no, name = findContact(contact_name)
                if contact_no:
                    whatsApp(contact_no, message_text, "mensagem", name)
                else:
                    speak("Não encontrei esse contato, Jéferson.")

            elif action == "fazer_ligacao":
                contact_name = params.get("contact_name", "")
                contact_no, name = findContact(contact_name)
                if contact_no:
                    whatsApp(contact_no, "", "chamada de voz", name)
                else:
                    speak("Não encontrei esse contato, Jéferson.")

            elif action == "video_call":
                contact_name = params.get("contact_name", "")
                contact_no, name = findContact(contact_name)
                if contact_no:
                    whatsApp(contact_no, "", "chamada de vídeo", name)
                else:
                    speak("Não encontrei esse contato, Jéferson.")

            # 🚨 Caso o Gemini retorne uma action ainda não mapeada
            else:
                speak("Ainda não sei como executar esse tipo de comando.")

                # 🤔 Nenhum comando reconhecido
                if not comando_valido:
                    speak("Desculpe, não entendi o comando. Pode tentar de novo?")
                    eel.ShowHood()
                    return  # evita loop infinito
            

           
        else : 
            speak("você precisa me chamar pelo nome, que é... sexta-feira")
            print("você não falou 'sexta-feira' ")
            
            ##Define o que fazer de acordo com a ação retornada pela IA"""
    
    # 🧠 Responder conversas normais


    except Exception as e:
        print("Erro ao processar comando:", e)
        speak("Houve um erro ao executar o comando, Jéferson.")
        eel.ShowHood()
        return

    eel.ShowHood()  # volta a exibir interface normalmente




