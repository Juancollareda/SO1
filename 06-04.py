import threading
import time
import random

class Estacion(threading.Thread):

    def __init__(self,nombre:str,evento_anterior:threading.Event,evento_siguiente:threading.Event):
        super().__init__()
        self.nombre = nombre
        self.evento_anterior = evento_anterior
        self.evento_siguiente = evento_siguiente

    def run(self):
        if self.evento_anterior:
            print(f'{self.nombre} está esperando a que finalice el proceso anterior', end="")
            self.evento_anterior.wait()

        tiempo_trabajo = random.uniform(1,3)
        print(f'{self.nombre} está trabajando (produciendo)....\n', end="")
        time.sleep(tiempo_trabajo)  # tiempo de trabajo simulado

        print(f'{self.nombre} ha terminado su trabajo.\n', end="")
        if self.evento_siguiente:
            self.evento_siguiente.set()

def main():
    evento1 = threading.Event()  # Est 1
    evento2 = threading.Event()  # Est 2
    evento3 = threading.Event()  # Est 3

    estacion1=Estacion("Estacion 1",None,evento1)
    estacion2=Estacion("Estacion 2",evento1,evento2)
    estacion3=Estacion("Estacion 3",evento2,evento3)

    estacion1.start()
    estacion2.start()
    estacion3.start()

    estacion1.join()
    estacion2.join()
    estacion3.join()
main()
