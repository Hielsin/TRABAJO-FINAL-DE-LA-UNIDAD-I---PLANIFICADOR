import random
from collections import deque

# Algoritmo de planificación SJF (Shortest Job First)
def sjf(processes):
    # Ordenar los procesos por tiempo de llegada
    sorted_processes = sorted(processes, key=lambda x: x['arrival_time'])
    return sorted_processes

# Algoritmo de planificación FCFS (First-Come, First-Served)
def fcfs(processes):
    # No se realiza ningún cambio en el orden de los procesos
    return processes

# Algoritmo de planificación SRFT (Shortest Remaining Time First)
def srft(processes):
    processes = deque(processes)
    scheduled_processes = []
    current_time = 0

    while processes:
        # Seleccionar el proceso con menor tiempo de ráfaga restante
        next_process = min(processes, key=lambda x: x['burst_time'])
        processes.remove(next_process)
        scheduled_processes.append(next_process)
        current_time += next_process['burst_time']

        # Actualizar los tiempos de ráfaga restante de los procesos en cola
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
        # Obtener el siguiente proceso de la cola
        process = processes.popleft()
        if process['burst_time'] > quantum:
            # Si el proceso aún tiene ráfaga restante después de un quantum,
            # se encola nuevamente al final
            process['burst_time'] -= quantum
            current_time += quantum
            processes.append(process)
        else:
            # Si el proceso completa su ráfaga antes de un quantum, se agrega a los procesos planificados
            current_time += process['burst_time']
            process['burst_time'] = 0
            scheduled_processes.append(process)

    return scheduled_processes

# Simulación de llegada de clientes con distribución uniforme
def simulate_client_arrival(num_clients, arrival_range):
    clients = []
    
    for i in range(num_clients):
        # Generar el tipo de cliente de forma aleatoria
        client_type = random.choice(['Cliente con tarjeta', 'Cliente sin tarjeta', 'Cliente preferencial'])
        
        if client_type == 'Cliente con tarjeta':
            # Si es cliente con tarjeta, seleccionar un subtipo aleatorio
            sub_types = ['Clientes con cuentas comunes', 'Clientes personas naturales VIP', 'Clientes personas jurídicas comunes', 'Clientes personas jurídicas VIP']
            sub_type = random.choice(sub_types)
        elif client_type == 'Cliente preferencial':
            # Si es cliente preferencial, seleccionar un subtipo aleatorio
            sub_types = ['Clientes mayores de 60 años', 'Clientes con deficiencia física', 'Clientes con necesidades especiales']
            sub_type = random.choice(sub_types)
        else:
            # Si no tiene tarjeta ni es preferencial, no hay subtipo
            sub_type = None
        
        # Generar tiempo de llegada y tiempo de ráfaga aleatorios
        arrival_time = random.uniform(arrival_range[0], arrival_range[1])
        burst_time = random.randint(1, 10)  # Duración de ráfaga aleatoria entre 1 y 10 unidades de tiempo
        
        # Crear el objeto cliente con la información generada
        client = {'arrival_time': arrival_time, 'burst_time': burst_time, 'client_type': client_type, 'sub_type': sub_type}
        clients.append(client)
    
    return clients

# Asignación de ventanillas a clientes
def assign_windows(clients, num_windows):
    # Crear las ventanillas con información adicional
    windows = [{'id': i + 1, 'busy': False, 'next_free_time': 0, 'times_idle': []} for i in range(num_windows)]
    scheduled_clients = []
    
    for client in clients:
        # Buscar ventanillas disponibles en el momento de llegada del cliente
        available_windows = [window for window in windows if window['next_free_time'] <= client['arrival_time']]
        
        if available_windows:
            # Asignar la primera ventanilla disponible al cliente
            window = min(available_windows, key=lambda x: x['next_free_time'])
            window['busy'] = True
            window['next_free_time'] = client['arrival_time'] + client['burst_time']
            client['assigned_window'] = window['id']
            scheduled_clients.append(client)
        else:
            # Si no hay ventanillas disponibles en el momento de llegada, se asigna None al cliente
            client['assigned_window'] = None
    
    return scheduled_clients

# Ejemplo de uso
def main():
    num_windows = int(input("Ingrese el número de ventanillas: "))
    clients = simulate_client_arrival(10, (0, 10))  # Simulación de 10 clientes
    scheduled_clients = assign_windows(clients, num_windows)
    
    print("Clientes asignados a ventanillas:")
    for client in scheduled_clients:
        if client['assigned_window'] is not None:
            print(f"Cliente: Tiempo de llegada: {client['arrival_time']}, Tiempo de ráfaga: {client['burst_time']}, Ventanilla asignada: {client['assigned_window']}")
        else:
            print(f"Cliente: Tiempo de llegada: {client['arrival_time']}, Tiempo de ráfaga: {client['burst_time']}, Sin ventanilla disponible")
    
if __name__ == '__main__':
    main()