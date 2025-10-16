import multiprocessing
import time

# Processo 1: roda o Eel e escuta a fila de ativação
def startJarvis(activate_q, done_q):
    print("Processo 1 (Eel) rodando")
    from main import start  # seu main.py
    start(activate_q, done_q)  # start precisa aceitar as filas

# Processo 2: roda o hotword
def listenHotword(activate_q, done_q):
    print("Processo 2 (Hotword) rodando")
    from engine.features import hotword
    hotword(activate_q, done_q)  # hotword adaptado para receber filas

if __name__ == '__main__':
    # Criação das filas
    activate_q = multiprocessing.Queue()
    done_q = multiprocessing.Queue()

    # Inicializa os processos passando as filas
    p1 = multiprocessing.Process(target=startJarvis, args=(activate_q, done_q), daemon=False)
    p2 = multiprocessing.Process(target=listenHotword, args=(activate_q, done_q), daemon=False)

    # Start dos processos
    p1.start()
    p2.start()

    # Aguarda o Eel terminar
    p1.join()

    # Se o processo do hotword ainda estiver ativo, encerra
    if p2.is_alive():
        p2.terminate()
        p2.join()

    print("System stop")


