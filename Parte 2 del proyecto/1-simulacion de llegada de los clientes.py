import random
from collections import deque

# Algoritmo de planificación SJF (Shortest Job First)
def sjf(processes):
    sorted_processes = sorted(processes, key=lambda x: x['arrival_time'])
    return sorted_processes

# Algoritmo de planificación FCFS (First-Come, First-Served)
def fcfs(processes):
    return processes

# Algoritmo de planificación SRFT (Shortest Remaining Time First)
def srft(processes):
    processes = deque(processes)
    scheduled_processes = []
    current_time = 0

    while processes:
        next_process = min(processes, key=lambda x: x['burst_time'])
        processes.remove(next_process)
        scheduled_processes.append(next_process)
        current_time += next_process['burst_time']

        for process in processes:
            if process['arrival_time'] <= current_time:
                process['burst_time'] -= current_time - process['arrival_time']

    return scheduled_processes

# Algoritmo de planificación RR (Round Robin)
def rr(processes, quantum):
    processes = deque(processes)
    scheduled_processes = []
    current_time = 0

    while processes:
        process = processes.popleft()
        if process['burst_time'] > quantum:
            process['burst_time'] -= quantum
            current_time += quantum
            processes.append(process)
        else:
            current_time += process['burst_time']
            process['burst_time'] = 0
            scheduled_processes.append(process)

    return scheduled_processes

# Simulación de llegada de clientes con distribución uniforme
def simulate_client_arrival(num_clients, arrival_range):
    clients = []
    
    for i in range(num_clients):
        arrival_time = random.uniform(arrival_range[0], arrival_range[1])
        burst_time = random.randint(1, 10)  # Duración de ráfaga aleatoria entre 1 y 10 unidades de tiempo
        clients.append({'arrival_time': arrival_time, 'burst_time': burst_time})
    
    return clients

# Ejemplo de uso
def main():
    num_clients = int(input("Ingrese el número de clientes a simular: "))
    arrival_range = (0, 10)  # Rango de tiempo de llegada (0 a 10 unidades de tiempo)
    quantum = 2  # Quantum para el algoritmo RR
    
    clients = simulate_client_arrival(num_clients, arrival_range)
    
    print("Selecciona un algoritmo de planificación:")
    print("1. SJF (Shortest Job First)")
    print("2. FCFS (First-Come, First-Served)")
    print("3. SRFT (Shortest Remaining Time First)")
    print("4. RR (Round Robin)")
    
    choice = int(input("Ingrese el número correspondiente al algoritmo: "))
    
    if choice == 1:
        scheduled_clients = sjf(clients)
    elif choice == 2:
        scheduled_clients = fcfs(clients)
    elif choice == 3:
        scheduled_clients = srft(clients)
    elif choice == 4:
        scheduled_clients = rr(clients, quantum)
    else:
        print("Opción no válida.")
        return
    
    print("\nClientes programados:")
    for i, client in enumerate(scheduled_clients):
        print(f"Cliente {i + 1}: Tiempo de llegada: {client['arrival_time']}, Tiempo de ráfaga: {client['burst_time']}")

if __name__ == '__main__':
    main()
