import threading

class Cine:
    def __init__(self):
        self.salas = []

    def agregar_sala(self, sala):
        self.salas.append(sala)

    def mostrar_salas(self):
        for index, sala in enumerate(self.salas):
            print(f"Sala {index + 1}:")
            sala.mostrar_asientos()


class Sala:
    def __init__(self, numero_sala):
        self.numero_sala = numero_sala
        self.asientos = {'A': [" ", " ", " "], 'B': [" ", " ", " "], 'C': [" ", " ", " "]}

    def mostrar_asientos(self):
        print(f"Estado de los asientos en la sala {self.numero_sala}:")
        for fila, asientos in self.asientos.items():
            print(f"{fila}: {asientos}")

    def buscar_vacio(self, fila, columna):
        return self.asientos[fila][columna] == " "

    def reservar_asiento(self, fila, columna):
        if self.buscar_vacio(fila, columna):
            self.asientos[fila][columna] = "X"
            print(f"Asiento {fila}{columna + 1} reservado con éxito.")
        else:
            print(f"El asiento {fila}{columna + 1} ya está ocupado.")


class Cliente(threading.Thread):
    lock = threading.Lock()  #esto se pone para bloquear 

    def __init__(self, nombre, sala):
        threading.Thread.__init__(self)
        self.nombre = nombre
        self.sala = sala
        self.reservas = []

    def reservar_asientos(self):
        while True:
            with Cliente.lock:  
                self.sala.mostrar_asientos()

                fila = input(f"{self.nombre}, elige la fila (A, B, C): ").upper()
                columna = int(input(f"{self.nombre}, elige el número de asiento (1, 2, 3): ")) - 1

                if fila in self.sala.asientos and 0 <= columna < len(self.sala.asientos[fila]):
                    self.sala.reservar_asiento(fila, columna)
                    self.reservas.append((fila, columna + 1))
                else:
                    print("Selección inválida.")

            otra = input("¿Quieres reservar otro asiento? (s/n): ").lower()
            if otra != 's':
                break

    def run(self):
        self.reservar_asientos()




cine = Cine()

sala1 = Sala(1)
cine.agregar_sala(sala1)


cliente1 = Cliente("Cliente 1", sala1)
cliente2 = Cliente("Cliente 2", sala1)


cliente1.start()
cliente2.start()


cliente1.join()
cliente2.join()

sala1.mostrar_asientos()

