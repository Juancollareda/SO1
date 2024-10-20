import threading
import time
import random

class RecursoCompartido:
    def __init__(self):
        self.data = 0
        self.lock = threading.Lock()
        self.readers_count = 0
        self.readers_count_lock = threading.Lock()
        self.read_turnstile = threading.Lock()

    def read_data(self):
        self.read_turnstile.acquire()
        self.read_turnstile.release()

        self.readers_count_lock.acquire()
        self.readers_count += 1
        if self.readers_count == 1:
            self.lock.acquire()
        self.readers_count_lock.release()

        # Simular la lectura del recurso
        read_value = self.data
        print(f"Recurso leído: {read_value}")

        self.readers_count_lock.acquire()
        self.readers_count -= 1
        if self.readers_count == 0:
            self.lock.release()
        self.readers_count_lock.release()

    def write_data(self, value):
        self.read_turnstile.acquire()
        self.lock.acquire()
        self.data = value
        print(f"Recurso escrito: {value}")
        self.lock.release()
        self.read_turnstile.release()

class Lector(threading.Thread):
    def __init__(self, recurso):
        super().__init__()
        self.recurso = recurso

    def run(self):
        while True:
            self.recurso.read_data()
            time.sleep(random.random())  # Simula tiempo de procesamiento

class Escritor(threading.Thread):
    def __init__(self, recurso, value):
        super().__init__()
        self.recurso = recurso
        self.value = value

    def run(self):
        while True:
            self.recurso.write_data(self.value)
            time.sleep(random.random())  # Simula tiempo de procesamiento

def main():
    recurso = RecursoCompartido()
    lectores = [Lector(recurso) for _ in range(5)]
    escritores = [Escritor(recurso, i) for i in range(3)]

    # Iniciar todos los lectores
    for lector in lectores:
        lector.start()

    # Iniciar todos los escritores
    for escritor in escritores:
        escritor.start()

    # Permitir que los hilos se ejecuten por un tiempo
    time.sleep(1)

    # No se detienen los hilos en este ejemplo. En un caso real, deberías incluir una manera de detener los hilos de manera segura.

if __name__ == "__main__":
    main()
            
            