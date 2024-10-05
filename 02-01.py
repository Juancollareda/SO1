import threading
import random

class MiThread(threading.Thread):
    def __init__(self,cantdenum):
        super().__init__()  
        self.cant = cantdenum
    def archivos(self, lista):
        with open("02-01.txt", "a") as arch:  
            for i in lista:
                arch.write(f"{i}\n")  
    
    def run(self):
        lista=[]
        for i in range(self.cant):
            lista.append(random.randint(0,10)**2)
        self.archivos(lista)

    

def main():
    t0=MiThread(3)
    t1=MiThread(2)
    t2=MiThread(4)
    t0.start()
    t0.join()
    t1.start()
    t1.join()
    t2.start()
    t2.join()
main()