import threading
import random
import time

def getTime():
    return time.perf_counter_ns()

num_corredores = 5
max_corredores_en_carrera = 3  
barrier_event = threading.Event()  
semaforo = threading.Semaphore(max_corredores_en_carrera)  # Semáforo para limitar el número de corredores

# Diccionario para almacenar los tiempos de cada corredor
tiempos_corredores = {"Proceso": getTime()}  # Guardar tiempo de inicio del proceso

class Corredor(threading.Thread):
    def __init__(self, id):
        super().__init__()
        self.id = id

    def run(self):
        print(f"Corredor {self.id} está listo para comenzar.")
        time.sleep(random.uniform(0.5, 2))  # Simular el tiempo que tarda en prepararse
        
        # Esperar a que todos los corredores estén listos
        barrier_event.wait()
        
        # Intentar obtener el semáforo para correr
        with semaforo:
            start_time = getTime()
            time.sleep(random.uniform(1, 3))  # Simular el tiempo de carrera
            end_time = getTime()
        
        
        tiempos_corredores[f"Corredor {self.id}"] = end_time - start_time

        # Imprimir mensaje cuando termine
        print(f"Corredor {self.id} ha terminado la carrera. Tiempo: {end_time - start_time:.2f} nanosegundos")

# Función para imprimir el análisis de tiempos de ejecución
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
        print(f'{k:10} {di[k]:035.25f}')    
    print("....................")
 
    dif = su - di["Proceso"]
    print(f'{"Difer.":10} {dif:+035.25f}')
    print("-" * 20)

# Función para esperar hasta que todos los corredores estén listos
def start_race():
    time.sleep(2) 
    print("¡Todos los corredores están listos! ¡Que comience la carrera!")
    barrier_event.set() 

corredores = []
for i in range(num_corredores):
    corredor = Corredor(i)
    corredores.append(corredor)
    corredor.start()

start_race()

# Esperar a que todos los corredores terminen
for corredor in corredores:
    corredor.join()

# Actualizar el tiempo final
tiempos_corredores["Proceso"] = getTime() - tiempos_corredores["Proceso"]

# Mostrar el análisis de tiempos
verTiempos(tiempos_corredores)

print("La carrera ha terminado.")
