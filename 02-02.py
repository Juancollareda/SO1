import threading
import random
import time

def getTime():
    '''
    #ns: nanosegundos -> '10**-9' o comunmente se escribe '1e-09'
    '''
    return time.perf_counter_ns()    
def verTiempos(di):
    '''
    Imprime una tabla con el análisis de tiempos de ejecución
    '''
    print("\n")
    print("-" * 20)
    print("Análisis de tiempos")
    print("....................")
    su = 0
    for k in di:
        if k != "Proceso":
            su += di[k]
        print(f'{k:10}{di[k]:035.25f}')    
    print("....................")
 
    dif = su - di["Proceso"]
    print(f'{"Difer.":10}{dif:+035.25f}')
    print("-" * 20)

class MiThread(threading.Thread):
    def __init__(self, cantdenum, nombre, tiempos):
        super().__init__()  
        self.cant = cantdenum
        self.nombre = nombre  
        self.tiempos = tiempos  
    
    def archivos(self, lista):
        with open("02-02.txt", "a") as arch:  
            for i in lista:
                arch.write(f"{i}\n")  
    
    def es_primo(self, num):
        if num < 2:
            return False
        for i in range(2, int(num**0.5) + 1):
            if num % i == 0:
                return False
        return True

    def buscar_primos(self, cantidad):
        primos = []
        num = 2  
        while len(primos) < cantidad:
            if self.es_primo(num):
                primos.append(num)
            num += 1
        return primos

    def run(self):
        print(f"Comienzo del hilo {self.nombre}\n", end="")
        tiempoInicio = getTime()  
        lista = self.buscar_primos(self.cant)
        self.archivos(lista)
        tiempoFin = getTime() - tiempoInicio  
        self.tiempos[self.nombre] = tiempoFin 
        print(f"Finalizado hilo {self.nombre}\n", end="")

def concurrente():
    tiempoIni = getTime()
    diTiempo = {}  

    t0 = MiThread(3, "Hilo 0", diTiempo)
    t1 = MiThread(5, "Hilo 1", diTiempo)
    t2 = MiThread(7, "Hilo 2", diTiempo)

 
    t0.start()
    t1.start()
    t2.start()

    t0.join()
    t1.join()
    t2.join()

    diTiempo["Proceso"] = getTime() - tiempoIni  # Tiempo total del proceso
    print("....................")
    print("FIN del Proceso Concurrente\n" + "-" * 20)
   
    verTiempos(diTiempo)


def secuencial():
    tiempoIni = getTime()
    diTiempo = {}  

    t0 = MiThread(3, "Hilo 0", diTiempo)
    t1 = MiThread(5, "Hilo 1", diTiempo)
    t2 = MiThread(7, "Hilo 2", diTiempo)

    t0.start()
    t0.join()

    t1.start()
    t1.join()

    t2.start()
    t2.join()

    diTiempo["Proceso"] = getTime() - tiempoIni  
    print("....................")
    print("FIN del Proceso Secuencial\n" + "-" * 20)

    verTiempos(diTiempo)
def main():
    print("\nEjecución Concurrente:")
    concurrente()  # Ejecuta el proceso de forma concurrente
    
    print("\nEjecución Secuencial:")
    secuencial()  # Ejecuta el proceso de forma secuencial
if __name__ == "__main__":
    main()



#Concurrente: Es mucho más eficiente en términos de tiempo total del proceso, lo cual es esperado ya que los hilos corren en paralelo.
#Secuencial: Tiene un mayor tiempo total de ejecución ya que cada hilo espera a que el anterior termine antes de comenzar.