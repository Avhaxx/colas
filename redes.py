import simpy
import random

# Clase clientes

class Cliente:
    def __init__(self, env, nodo, mu, nombre):
        self.env = env
        self.nodo = nodo
        self.mu = mu
        self.nombre = nombre
        self.inicio_atencion_time = 0
        self.fin_atencion_time = 0
        self.action = env.process(self.llegada())

    def llegada(self):
        with self.nodo.resource.request() as req:
            yield req
            self.inicio_atencion_time = round (self.env.now, 4)
            yield self.env.timeout(random.expovariate(self.mu))
            self.fin_atencion_time = round(self.env.now, 4)
    
    def get_fin(self):
        return {
            'Nombre': self.nombre, 
            'Inicio atencion': self.inicio_atencion_time, 
            'Fin atencion': self.fin_atencion_time
        }

# Clase Nodo

class Nodo:
    def __init__(self, env, nombre, capacidad):
        self.env = env
        self.name = nombre
        self.resource = simpy.Resource(env, capacity=capacidad)

# Configuración de la simulación
env = simpy.Environment()


