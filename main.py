import os
import threading
import time
import eel
import random
from engine.command import speak



from engine.features import playAssistantSound



def start(activate_q, done_q):
    eel.init('www')

    playAssistantSound()

    # abre o navegador
    os.system('start msedge.exe --app="http://localhost:8000"')

    # inicia thread que monitora a fila de ativação da hotword
    monitor_thread = threading.Thread(target=monitor_activate_queue, args=(activate_q, done_q), daemon=True)
    monitor_thread.start()

    # inicia o Eel (bloqueia a thread principal)
    eel.start('index.html', mode=None, host='localhost', block=True)


def monitor_activate_queue(activate_q, done_q):
    import random
    import time
    from engine.features import playAssistantSound
    from engine.command import takeCommand, allCommands
    

    # 🔸 Lista de falas femininas e naturais
    frases = [
    "Oi, Jéferson!",
    "Fala, Jéferson!",
    "Oi, Jéferson, tudo bem?",
    "Tô aqui, Jéferson.",
    "Pode falar, Jéferson.",
    "Oi, Jéferson! Diga.",
    "Opa, Jéferson!",
    "Oi de novo, Jéferson!",
    "E aí, Jéferson!",
    "Tô te ouvindo, Jéferson."
    ]

    while True:
        try:
            msg = activate_q.get()  # espera hotword
            if msg == 'hotword':
                print("Hotword detectada! Chamando takeCommand()...")

                # 🔊 Escolhe uma saudação aleatória
                fala = random.choice(frases)
                print(fala)  # exibe no console (opcional)

                # 🔊 toca o som de ativação
                playAssistantSound()
                speak(fala)
                try:
                    if hasattr(eel, 'DisplayMessage'):
                        eel.DisplayMessage(fala)  # mostra a frase na tela
                        eel.DisplayMessage("Ouvindo...")

                    query = takeCommand()
                    if query:
                        allCommands(query)
                    else:
                        print("Nenhum comando reconhecido.")
                except Exception as e:
                    print("Erro no takeCommand/allCommands:", e)
                finally:
                    done_q.put('done')  # sinaliza para o hotword continuar
        except Exception as e:
            print("Erro monitor queue:", e)
            time.sleep(0.5)

