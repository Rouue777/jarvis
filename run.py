import multiprocessing


# runs sexta feira
def startJarvis():
    #code processo 1
    print("processo 1 rodando")
    from main import start
    start()

#run hot word
def listenHotword():
    #code processo 2
    print("processo 2 rodando")
    from engine.features import hotword
    hotword()


    # Start both processes
if __name__ == '__main__':
        p1 = multiprocessing.Process(target=startJarvis)
        p2 = multiprocessing.Process(target=listenHotword)
        p1.start()
        p2.start()
        p1.join()

        if p2.is_alive():
            p2.terminate()
            p2.join()

        print("system stop")