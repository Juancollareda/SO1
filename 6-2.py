import threading
import random
import time

class MessageProducer(threading.Thread):
    def __init__(self, buffer, cantMensajes, conditional):
        super().__init__()
        self.buffer=buffer
        self.cantMensajes=cantMensajes
        self.conditional=conditional

    def run(self):
        for i in range (self.cantMensajes):
            time.sleep(random.uniform(0.5,1.5))
            mensaje=f'Mensaje {i}'
            with self.conditional:
                self.buffer.append(mensaje)
                print(f"Productor produjo: {mensaje}")
                self.conditional.notify()

class MessageConsumer(threading.Thread):
    def __init__(self, buffer, cantMensajes, conditional):
        super().__init__()
        self.buffer=buffer
        self.cantMensajes=cantMensajes
        self.conditional=conditional
    
    def run(self):
        for i in range (self.cantMensajes):
            with self.conditional:
                while not self.buffer:
                    self.conditional.wait()
                mensaje=self.buffer.pop(0)
                print(f"Consumidor uso: {mensaje}")
            time.sleep(random.uniform(0.5,2))


def main():
    cantMensajes=6
    buffer=[]
    conditional=threading.Condition()
    MP= MessageProducer(buffer, cantMensajes, conditional)
    MC= MessageConsumer(buffer, cantMensajes, conditional)
    MP.start()
    MC.start()
    MP.join()
    MC.join()

if __name__=="__main__":
    main()