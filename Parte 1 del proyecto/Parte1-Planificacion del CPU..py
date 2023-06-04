import matplotlib.pyplot as plt
import pandas as pd
from collections import deque

class Proceso:
    def __init__(self, nombre, tiempo_llegada, duracion):
        self.nombre = nombre
        self.tiempo_llegada = tiempo_llegada
        self.duracion = duracion

def planificador_sjf(procesos):
    procesos.sort(key=lambda x: x.duracion)

    tiempo_total = 0
    tiempo_espera_total = 0
    gantt_data = []

    print("Proceso\tTiempo llegada\tDuración\tTiempo espera")

    for proceso in procesos:
        if tiempo_total < proceso.tiempo_llegada:
            tiempo_total = proceso.tiempo_llegada

        tiempo_espera = tiempo_total - proceso.tiempo_llegada
        print(proceso.nombre, "\t\t", proceso.tiempo_llegada, "\t\t", proceso.duracion, "\t\t", tiempo_espera)

        gantt_data.append([proceso.nombre, tiempo_total, tiempo_total + proceso.duracion])

        tiempo_total += proceso.duracion
        tiempo_espera_total += tiempo_espera

    tiempo_promedio_espera = tiempo_espera_total / len(procesos)

    print("\nTiempo total:", tiempo_total)
    print("Tiempo promedio de espera:", tiempo_promedio_espera)

    df = pd.DataFrame(gantt_data, columns=["Proceso", "Inicio", "Fin"])
    plot_gantt_chart(df)

def planificador_fcfs(procesos):
    procesos.sort(key=lambda x: x.tiempo_llegada)

    tiempo_total = 0
    tiempo_espera_total = 0
    gantt_data = []

    print("Proceso\tTiempo llegada\tDuración\tTiempo espera")

    for proceso in procesos:
        if tiempo_total < proceso.tiempo_llegada:
            tiempo_total = proceso.tiempo_llegada

        tiempo_espera = tiempo_total - proceso.tiempo_llegada
        print(proceso.nombre, "\t\t", proceso.tiempo_llegada, "\t\t", proceso.duracion, "\t\t", tiempo_espera)

        gantt_data.append([proceso.nombre, tiempo_total, tiempo_total + proceso.duracion])

        tiempo_total += proceso.duracion
        tiempo_espera_total += tiempo_espera

    tiempo_promedio_espera = tiempo_espera_total / len(procesos)

    print("\nTiempo total:", tiempo_total)
    print("Tiempo promedio de espera:", tiempo_promedio_espera)

    df = pd.DataFrame(gantt_data, columns=["Proceso", "Inicio", "Fin"])
    plot_gantt_chart(df)

def planificador_srft(procesos):
    tiempo_total = 0
    tiempo_espera_total = 0
    gantt_data = []
    procesos_terminados = []

    print("Proceso\tTiempo llegada\tDuración\tTiempo espera")

    while len(procesos) > 0:
        procesos.sort(key=lambda x: x.duracion)
        proceso_actual = procesos[0]

        if tiempo_total < proceso_actual.tiempo_llegada:
            tiempo_total = proceso_actual.tiempo_llegada

        tiempo_espera = tiempo_total - proceso_actual.tiempo_llegada
        print(proceso_actual.nombre, "\t\t", proceso_actual.tiempo_llegada, "\t\t", proceso_actual.duracion, "\t\t", tiempo_espera)

        gantt_data.append([proceso_actual.nombre, tiempo_total, tiempo_total + 1])

        proceso_actual.duracion -= 1
        tiempo_total += 1

        if proceso_actual.duracion == 0:
            procesos_terminados.append(proceso_actual)
            procesos.pop(0)

    for proceso in procesos_terminados:
        tiempo_espera_total += tiempo_total - proceso.tiempo_llegada

    tiempo_promedio_espera = tiempo_espera_total / len(procesos_terminados)

    print("\nTiempo total:", tiempo_total)
    print("Tiempo promedio de espera:", tiempo_promedio_espera)

    df = pd.DataFrame(gantt_data, columns=["Proceso", "Inicio", "Fin"])
    plot_gantt_chart(df)

def planificador_rr(procesos, quantum):
    tiempo_total = 0
    tiempo_espera_total = 0
    gantt_data = []
    procesos_listos = deque(procesos)
    procesos_terminados = []

    print("Proceso\tTiempo llegada\tDuración\tTiempo espera")

    while len(procesos_listos) > 0:
        proceso_actual = procesos_listos.popleft()

        if tiempo_total < proceso_actual.tiempo_llegada:
            tiempo_total = proceso_actual.tiempo_llegada

        tiempo_espera = tiempo_total - proceso_actual.tiempo_llegada
        print(proceso_actual.nombre, "\t\t", proceso_actual.tiempo_llegada, "\t\t", proceso_actual.duracion, "\t\t", tiempo_espera)

        duracion_restante = proceso_actual.duracion if proceso_actual.duracion <= quantum else quantum
        gantt_data.append([proceso_actual.nombre, tiempo_total, tiempo_total + duracion_restante])

        proceso_actual.duracion -= duracion_restante
        tiempo_total += duracion_restante

        if proceso_actual.duracion > 0:
            procesos_listos.append(proceso_actual)
        else:
            procesos_terminados.append(proceso_actual)

    for proceso in procesos_terminados:
        tiempo_espera_total += tiempo_total - proceso.tiempo_llegada

    tiempo_promedio_espera = tiempo_espera_total / len(procesos_terminados)

    print("\nTiempo total:", tiempo_total)
    print("Tiempo promedio de espera:", tiempo_promedio_espera)

    df = pd.DataFrame(gantt_data, columns=["Proceso", "Inicio", "Fin"])
    plot_gantt_chart(df)

def plot_gantt_chart(df):
    fig, ax = plt.subplots()
    ax.set_title("Diagrama de Gantt")
    ax.grid(True)
    ax.set_xlabel("Tiempo")
    ax.set_ylabel("Proceso")

    for i, row in df.iterrows():
        ax.barh(row["Proceso"], width=row["Fin"] - row["Inicio"], left=row["Inicio"], height=0.5)

    plt.show()

def menu():
    print("=== Algoritmos de Planificación ===")
    print("1. SJF (Shortest Job First)")
    print("2. FCFS (First-Come, First-Served)")
    print("3. SRFT (Shortest Remaining Time First)")
    print("4. RR (Round Robin)")
    print("0. Salir")

    opcion = input("Seleccione un algoritmo de planificación (0-4): ")

    if opcion == "1":
        ejecutar_algoritmo(planificador_sjf)
    elif opcion == "2":
        ejecutar_algoritmo(planificador_fcfs)
    elif opcion == "3":
        ejecutar_algoritmo(planificador_srft)
    elif opcion == "4":
        quantum = int(input("Ingrese el valor del quantum: "))
        ejecutar_algoritmo(lambda p: planificador_rr(p, quantum))
    elif opcion == "0":
        print("¡Hasta luego!")
        return
    else:
        print("Opción inválida. Por favor, seleccione nuevamente.")
    
    menu()

def ejecutar_algoritmo(algoritmo):
    num_procesos = int(input("Ingrese el número de procesos: "))
    lista_procesos = []

    for i in range(num_procesos):
        nombre = input("Ingrese el nombre del proceso {}: ".format(i + 1))
        tiempo_llegada = int(input("Ingrese el tiempo de llegada del proceso {}: ".format(i + 1)))
        duracion = int(input("Ingrese la duración del proceso {}: ".format(i + 1)))

        proceso = Proceso(nombre, tiempo_llegada, duracion)
        lista_procesos.append(proceso)

    algoritmo(lista_procesos)

menu()
