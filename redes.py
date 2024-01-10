import simpy
import random

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
        #print(f"Llega el cliente {self.nombre} al nodo {self.nodo.name} en el tiempo {round(self.env.now, 4)}")
        with self.nodo.resource.request() as req:
            yield req
            self.inicio_atencion_time = round (self.env.now, 4)
            #print(f"El cliente {self.nombre} comienza a ser atendido en el {self.nodo.name} en el tiempo {round(self.env.now, 4)}")
            yield self.env.timeout(random.expovariate(self.mu))
            self.fin_atencion_time = round(self.env.now, 4)
            #print(f"El cliente ha sido atendido y deja el {self.nodo.name} en el tiempo {round(self.env.now, 4)}")
            #print(f" Tiempo de inicio de atención: {self.inicio_atencion_time}, Tiempo de fin de atención: {self.fin_atencion_time}\n")
        
    def get_fin(self):
        return {
            'Nombre': self.nombre, 
            'Inicio atencion': self.inicio_atencion_time, 
            'Fin atencion': self.fin_atencion_time
        }

class Nodo:
    def __init__(self, env, nombre, capacidad):
        self.env = env
        self.name = nombre
        self.resource = simpy.Resource(env, capacity=capacidad)

# Configuración de la simulación
env = simpy.Environment()


