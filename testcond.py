'''
CONDITION
Simularemos una situación en la que un productor genera datos y un consumidor
espera a que los datos estén disponibles para procesarlos (consumirlo).

Clase Producer:
    El Producer (productor) produce datos y los agrega a la lista data. Después de producir
    cada ítem, el productor adquiere la condición con with self.condition, agrega el ítem a data,
    y luego notifica al consumidor con self.condition.notify().

Clase Consumer:
    El Consumer (consumidor) espera a que haya datos en la lista data. Si no hay datos disponibles,
    el consumidor espera a que el productor lo notifique usando self.condition.wait(). Cuando recibe
    la notificación, consume el ítem (lo elimina de la lista data).

Sincronización con Condition:
    La Condition se usa para sincronizar la producción y el consumo.
    El productor notifica cuando hay nuevos datos, y el consumidor espera hasta que recibe esa
    notificación para procesar los datos.

Espera Activa y Notificación:
    El consumidor utiliza un bucle while not self.data: para verificar si hay datos disponibles.
    Esto evita que el consumidor continúe antes de que el productor haya agregado nuevos datos.

Finalización:
    Después de producir y consumir 5 ítems, ambos hilos terminan su ejecución, y se imprime un mensaje final.

Métodos de la clase threading.Condition()

    .notify(): cuando se ejecuta habilita a los threadd en espera  a continuar su ejecución.
    .wait():  Cuando se ejecuta mantendrá en espera el thread hasta que se emita la notificacion de la condicion 


'''
import threading
import time
import random

class Producer(threading.Thread):
    def __init__(self, condition, data):
        super().__init__()
        self.condition = condition
        self.data = data

    def run(self):
        for _ in range(5):                      # Producir 5 ítems
            time.sleep(random.uniform(0.05, 0.2))  # Simula el tiempo de producción
            with self.condition:                # Cuando termina el bloque with ejecuta 'self.condition.release()'
                item = random.randint(1, 100)
                self.data.append(item)          # agrega / carga números en la lista
                print(f"Productor produjo: {item}\n",end="")
                self.condition.notify()         # Notifica al consumidor que hay datos disponibles
                                                # Notifica la CONDICION

class Consumer(threading.Thread):
    def __init__(self, condition, data):
        super().__init__()
        self.condition = condition
        self.data = data

    def run(self):
        for _ in range(5):                       # Consumir 5 ítems
            with self.condition:                 # Cuando termina el bloque with ejecuta 'self.condition.release()'
                while not self.data:             # Espera a que haya datos disponibles
                    self.condition.wait()        # Espera a que el productor notifique
                                                 # Espera la notificación de la CONDICION
                item = self.data.pop(0)          # elimina los numeros de la lista
                print(f"Consumidor consumió: {item}\n",end="")
            time.sleep(random.uniform(0.5, 2))   # Simula el tiempo de procesamiento

def main():
    condition = threading.Condition()            # Instancia de Condition
    data = []                                    # Lista que se utilizará en el thread de Producer para cargar (escribir)
                                                 # y en el thread de Consumer para descargar (leer)

    producer = Producer(condition, data)         # Instancia de Producer en un thread
    consumer = Consumer(condition, data)         # Instancia de Producer en otro thread

    producer.start()
    consumer.start()

    producer.join()
    consumer.join()

    print("Producción y consumo han finalizado.",end="")

if __name__ == "__main__":
    main()
    