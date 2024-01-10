import simpy
import random
class Simulacion:

    def __init__(self, servidores, tasa_llegada, tasa_servicio):
        self.servidores = servidores
        self.tasa_llegada = tasa_llegada
        self.tasa_servicio = tasa_servicio

        self.env = simpy.Environment()
        self.servidor = simpy.Resource(self.env, capacity=self.servidores)
        self.tiempo_en_sistema = []

        self.tiempo_promedio_sistema = 0
        self.utilizacion_servidores = 0

    def get_tiempo_promedio(self):
        return self.tiempo_promedio_sistema

    def get_utilizacion(self):
        return self.utilizacion_servidores

    def cliente(self, env, servidor):
        self.llegada = env.now
        with servidor.request() as req:
            yield req
            self.servicio = random.expovariate(self.tasa_servicio)
            yield env.timeout(self.servicio)
        self.salida = self.env.now
        self.tiempo_en_sistema.append(self.salida - self.llegada)


    def generar_clientes(self, env, tasa_llegada, servidor):
        
        for i in range(100):
            self.env.process(self.cliente(self.env, self.servidor))
            self.inter_llegada = random.expovariate(self.tasa_llegada)
            yield env.timeout(self.inter_llegada)

    def empezar(self):
        """
        The function "empezar" generates clients and calculates the average time in the system and the
        utilization of servers.
        """
        self.env.process(self.generar_clientes(self.env, self.tasa_llegada, self.servidor))
        self.env.run()

        self.tiempo_promedio_sistema = sum(self.tiempo_en_sistema) / len(self.tiempo_en_sistema)
        self.utilizacion_servidores = sum(self.tiempo_en_sistema) / (self.servidores * self.env.now)

        #print("Tiempo promedio en el sistema:", tiempo_promedio_sistema)
        #print("Utilización de los servidores:", utilizacion_servidores)


instancia = Simulacion(30, 10, 15)

instancia.empezar()



