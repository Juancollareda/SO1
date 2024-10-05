import threading
import os
import time

class MonitorDirectorio(threading.Thread):
    def __init__(self, directorio):
        super().__init__()
        self.directorio = directorio
        self.daemon = True  # Configura el hilo como demonio
        self.archivos_previos = set(os.listdir(directorio))

    def run(self):
        while True:
            archivos_actuales = set(os.listdir(self.directorio))
            nuevos_archivos = archivos_actuales - self.archivos_previos

            if nuevos_archivos:
                with open("registro_log.txt", "a") as log:
                    for archivo in nuevos_archivos:
                        log.write(f"Archivo nuevo: {archivo}\n")
                        print(f"Archivo nuevo detectado: {archivo}")

            self.archivos_previos = archivos_actuales
            time.sleep(5)  # Pausa de 5 segundos entre cada verificación

def menu_usuario():
    while True:
        print("\nMenú del Usuario:")
        print("1. Agregar un archivo ficticio al directorio")
        print("2. Salir")
        opcion = input("Elige una opción: ")

        if opcion == "1":
            archivo_nuevo = f"archivo_ficticio_{int(time.time())}.txt"
            with open(os.path.join("directorio_monitor", archivo_nuevo), "w") as f:
                f.write("Este es un archivo .\n")
            print(f"{archivo_nuevo} agregado al directorio.")
        elif opcion == "2":
            print("Saliendo...")
            break
        else:
            print("Opción no válida.")

def main():
    directorio = "directorio_monitor"
    
    # Crear el directorio si no existe
    if not os.path.exists(directorio):
        os.makedirs(directorio)

    # Iniciar el hilo demonio
    monitor = MonitorDirectorio(directorio)
    monitor.start()

    # Permitir al usuario realizar otras tareas mientras el monitor funciona en segundo plano
    menu_usuario()

if __name__ == "__main__":
    main()
