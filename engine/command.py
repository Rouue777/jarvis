import pyttsx3
import speech_recognition as sr
import eel
import time
from engine.gemini import chat_with_gemini






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
        if "sexta-feira" in query.lower():
            print(query)
            response = chat_with_gemini(query)
            speak(response)

            comando_valido = True
           

        elif "abrir" in query.lower():
            from engine.features import openCommand
            openCommand(query)
            comando_valido = True

        # 🎵 Spotify
        elif "spotify" in query.lower() or "no spotify" in query.lower():
            if any(word in query.lower() for word in ["toca", "joga", "jogar", "tocar", "reproduzir"]):
                if "playlist" in query.lower() or "playlists" in query.lower():
                    from engine.spotify import play_playlist
                    print("Spotify Play Playlist =", query)
                    play_playlist(query)
                else:
                    from engine.spotify import playSpotify
                    print("Spotify Play Música =", query)
                    playSpotify(query)
            elif any(word in query.lower() for word in ["pause", "pausar", "parar"]):
                from engine.spotify import pauseSpotify
                print("Spotify Pause =", query)
                pauseSpotify()
            elif any(word in query.lower() for word in ["next", "próxima", "pular"]):
                from engine.spotify import next_track
                next_track()
            elif any(word in query.lower() for word in ["voltar", "anterior", "música anterior"]):
                from engine.spotify import previous_track
                previous_track()
            elif any(word in query.lower() for word in ["play", "resumir", "continuar"]):
                from engine.spotify import resumeSpotify
                resumeSpotify()
            comando_valido = True

        # ▶️ YouTube
        elif "youtube" in query.lower() and any(word in query.lower() for word in ["play", "tocar", "reproduzir"]):
            from engine.features import PlayYoutube
            print("YouTube Play =", query)
            PlayYoutube(query)
            comando_valido = True

        # 💬 WhatsApp
        elif any(word in query.lower() for word in [
            "enviar mensagem", "mandar mensagem", "ligar", "fazer ligação", "chamada de vídeo"
        ]):
            contact_no, name = findContact(query)
            if contact_no != 0:
                flag = ""
                message_text = ""
                if "mensagem" in query:
                    speak("Qual mensagem você quer enviar?")
                    message_text = takeCommand()
                    flag = 'mensagem'
                elif "ligar" in query or "fazer ligação" in query:
                    flag = 'chamada de voz'
                elif "vídeo" in query:
                    flag = 'chamada de vídeo'

                whatsApp(contact_no, message_text, flag, name)
            else:
                speak("Não encontrei esse contato, Jéferson.")
            comando_valido = True

        # 🤔 Nenhum comando reconhecido
        if not comando_valido:
            speak("Desculpe, não entendi o comando. Pode tentar de novo?")
            eel.ShowHood()
            return  # evita loop infinito

    except Exception as e:
        print("Erro ao processar comando:", e)
        speak("Houve um erro ao executar o comando, Jéferson.")
        eel.ShowHood()
        return

    eel.ShowHood()  # volta a exibir interface normalmente




