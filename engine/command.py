import pyttsx3
import speech_recognition as sr
import eel
import time



def speak(text):   
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)  # Change index to change voices. 0 for
    engine.setProperty('rate', 200)  # Speed percent (can go over 100)
    eel.DisplayMessage(text)
    engine.say(text)
    eel.receiverText(text)
    engine.runAndWait()

@eel.expose
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('listening...')
        eel.DisplayMessage('listening...')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        try:
            audio = r.listen(source, timeout=30, phrase_time_limit=6)
        except sr.WaitTimeoutError:
            print("Listening timed out while waiting for phrase to start.")
            return ""

    try:
        print('Recognizing...')
        eel.DisplayMessage('Recognizing...')
        query = r.recognize_google(audio, language='pt-br')
        print(f'User said: {query}\n')
        eel.DisplayMessage(query)
        time.sleep(2)
       
        return query
    except Exception as e:
        print("Could not recognize speech:", e)
        return ""
    


@eel.expose
def allCommands(message=1):
    from engine.features import findContact, whatsApp

    while True:

        if message == 1:
            query = takeCommand()
            print(query)
            eel.senderText(query)
        else:
            query = message
            eel.senderText(query)
            

        try:
            if "abrir" in query.lower():
                from engine.features import openCommand
                openCommand(query)

            elif "no youtube" in query.lower() or "tocar" in query.lower() or "play" in query.lower():
                from engine.features import PlayYoutube
                PlayYoutube(query)

            elif ("enviar mensagem" in query.lower() or 
                  "mandar mensagem" in query.lower() or 
                  "ligar" in query.lower() or 
                  "fazer ligação" in query.lower() or
                  "chamada de vídeo" in query.lower()):

                contact_no, name = findContact(query)

                if contact_no != 0:
                    # Inicializa a flag e a mensagem
                    flag = ""
                    message_text = ""

                    if "enviar mensagem" in query or "mandar mensagem" in query:
                        print(query)
                        flag = 'mensagem'
                        speak("Qual mensagem você quer enviar?")
                        message_text = takeCommand()  # aqui você captura a mensagem do usuário

                    elif "ligar" in query or "fazer ligação" in query:
                        flag = 'chamada de voz'

                    elif "chamada de vídeo" in query or "vídeo" in query:
                        flag = 'chamada de vídeo'

                    # Chama a função whatsapp apenas uma vez, com os parâmetros corretos
                    whatsApp(contact_no, message_text, flag, name)

                else:
                    speak("Não consegui encontrar esse contato.")

            else:
                speak("Desculpe, não entendi o comando. Pode repetir?")
                continue  # volta a ouvir sem precisar chamar hotword

        except Exception as e:
            print("erro no comando", e)

        eel.ShowHood()
        break  # sai do loop depois de executar um comando válido


