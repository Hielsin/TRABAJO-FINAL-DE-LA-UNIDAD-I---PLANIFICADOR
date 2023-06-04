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
        client_type = random.choice(['Cliente con tarjeta', 'Cliente sin tarjeta', 'Cliente preferencial'])
        
        if client_type == 'Cliente con tarjeta':
            sub_types = ['Clientes con cuentas comunes', 'Clientes personas naturales VIP', 'Clientes personas jurídicas comunes', 'Clientes personas jurídicas VIP']
            sub_type = random.choice(sub_types)
        elif client_type == 'Cliente preferencial':
            sub_types = ['Clientes mayores de 60 años', 'Clientes con deficiencia física', 'Clientes con necesidades especiales']
            sub_type = random.choice(sub_types)
        else:
            sub_type = None
        
        arrival_time = random.uniform(arrival_range[0], arrival_range[1])
        burst_time = random.randint(1, 10)  # Duración de ráfaga aleatoria entre 1 y 10 unidades de tiempo
        
        client = {'arrival_time': arrival_time, 'burst_time': burst_time, 'client_type': client_type, 'sub_type': sub_type}
        clients.append(client)
    
    return clients

# Simulación del funcionamiento de ventanillas
def simulate_windows(num_windows):
    windows = [{'id': i + 1, 'busy': False, 'next_free_time': 0, 'times_idle': []} for i in range(num_windows)]
    clients = simulate_client_arrival(10, (0, 10))  # Simulación de 10 clientes
    
    for client in clients:
        window = min(windows, key=lambda x: x['next_free_time'])
        
        if window['busy']:
            idle_time = window['next_free_time'] - client['arrival_time']
            window['times_idle'].append(idle_time)
            window['next_free_time'] += client['burst_time']
        else:
            window['busy'] = True
            window['next_free_time'] = client['arrival_time'] + client['burst_time']
    
    total_idle_time = sum(sum(window['times_idle']) for window in windows)
    avg_idle_time = total_idle_time / num_windows
    
    print("Ventanillas:")
    for window in windows:
        print(f"Ventanilla {window['id']}: Tiempos de inactividad: {window['times_idle']}")
    
    print(f"\nTiempo total de inactividad de las ventanillas: {total_idle_time}")
    print(f"Tiempo promedio de inactividad por ventanilla: {avg_idle_time}")

# Ejemplo de uso
def main():
    num_windows = int(input("Ingrese el número de ventanillas: "))
    simulate_windows(num_windows)

if __name__ == '__main__':
    main()
