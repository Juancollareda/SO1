import threading
import time 
import random

class Productor(threading.Thread):
    def __init__(self,dato,cantProduc,semaforo):
        super().__init__()
        self.dato=dato
        self.cantProduc=cantProduc
        self.semaforo=semaforo
       
        

    

    def run(self):
        for i in range(0,self.cantProduc):
            numero=random.randint(0,10)
            self.dato.append(numero)
            print(f"produsco: {numero}")
            self.semaforo.release()



class Consumidor(threading.Thread):
    def __init__(self,dato,cantProduc,semaforo):
        super().__init__()
        self.dato=dato
        self.cantProduc=cantProduc
        self.semaforo=semaforo
       
        

    

    def run(self):

        for i in range(0,self.cantProduc):
            self.semaforo.acquire()
            item=self.dato.pop(0)
            print(f"consumiendo: {item}")



def main():
    dato=[]
    cant=10
    semaforo=threading.Semaphore(0)
    productor=Productor(dato,cant,semaforo)
    consumidor=Consumidor(dato,cant,semaforo)
    productor.start()
    consumidor.start()
    productor.join()
    consumidor.join()



main()