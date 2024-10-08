import threading
import time

class CajaDeAhorro:
    def __init__(self):
        self.saldo = 100  

    def depositar(self, monto):
        self.saldo += monto

    def retirar(self, monto):
        self.saldo -= monto

    def obtener_saldo(self):
        return self.saldo

class Usuario(threading.Thread):
    def __init__(self, name, thread_lock, caja, accion, monto):
        threading.Thread.__init__(self)
        self.name = name
        self.accion = accion
        self.monto = monto
        self.thread_lock = thread_lock
        self.caja = caja  # Caja compartida

    def run(self):
        print(f'Starting thread {self.name}.\n')
        with self.thread_lock:  
            if self.accion == "+":
                self.caja.depositar(self.monto)
            else:
                self.caja.retirar(self.monto)
            time.sleep(0.5)  
            print(f'Thread {self.name} saldo actual: {self.caja.obtener_saldo()}\n')
        print(f'Finished thread {self.name}.\n')

def main():
    thread_lock = threading.Lock()
    caja = CajaDeAhorro()  

    # Crear hilos
    thread1 = Usuario('A', thread_lock, caja, "+", 50)
    thread2 = Usuario('B', thread_lock, caja, "-", 20)

    
    thread1.start()
    thread2.start()

    
    thread1.join()
    thread2.join()

    print(f'Saldo final en la caja: {caja.obtener_saldo()}')
    print('Termine.')

if __name__ == "__main__":
    main()
