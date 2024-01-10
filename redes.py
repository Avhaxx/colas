import simpy
import random

class Cliente:
    def __init__(self, env, nombre, nodo, mu):
        self.env = env
        self.nombre = nombre
        self.nodo = nodo
        self.mu = mu
        self.inicio_atencion_time = 0
        self.fin_atencion_time = 0
        self.action = env.process(self.llegada())

    def llegada(self):
        with self.nodo.resource.request() as req:
            yield req
            self.inicio_atencion_time = round(self.env.now, 4)
            print(f"El cliente {self.nombre} comienza a ser atendido en el {self.nodo.name} en el tiempo {round(self.env.now, 4)}")
            yield self.env.timeout(random.expovariate(self.mu))
            self.fin_atencion_time = round(self.env.now, 4)
            print(f"El cliente {self.nombre} ha sido atendido y deja el {self.nodo.name} en el tiempo {round(self.env.now, 4)}")
            print(f" Tiempo de inicio de atención: {self.inicio_atencion_time}, Tiempo de fin de atención: {self.fin_atencion_time}\n")
            return self.inicio_atencion_time
        
    def __gt__(self, other):
    # Define the comparison logic based on the attributes of the Cliente class
    # For example, if Cliente instances have an attribute 'mu' representing service time, you can compare based on service time
        return self.mu > other.mu

class Nodo:
    def __init__(self, env, nombre, capacidad):
        self.env = env
        self.name = nombre
        self.resource = simpy.Resource(env, capacity=capacidad)

class Interconexion:
    def __init__(self):
        self.env = simpy.Environment()
        self.nodo1 = Nodo(self.env, 'Nodo 1', 1)
        self.nodo2 = Nodo(self.env, 'Nodo 2', 1)
        self.esperar = []

    def ejecutar_simulacion(self):
        for i in range(100):
            cliente1 = Cliente(self.env, f'Cliente {i}', self.nodo1, random.uniform(0.1, 5.0))
            cliente2 = Cliente(self.env, f'Cliente {i}', self.nodo2, random.uniform(0.1, 5.0))
            if (cliente1 > cliente2):
                self.esperar.append(cliente2);
        self.env.run(until=1000)
        self.calcular_probabilidad()
    
    def calcular_probabilidad(self):
        service_times = [cliente.mu for cliente in self.esperar]
        probabilidad = sum(service_times) / len(service_times)
        print(f'El promedio del tiempo de espera entre nodos es: {round(probabilidad, 4)}')
        return probabilidad
    
# Crear una instancia de la simulación y ejecutarla
sim = Interconexion()
sim.ejecutar_simulacion()
