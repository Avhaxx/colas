from fastapi import FastAPI, Request
from simulacion import Simulacion
from pydantic import BaseModel
from redes import Interconexion
import simpy
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Body(BaseModel):
    servidores: int
    tasa_llegada: int
    tasa_servicio: int


""" class Nodo(BaseModel):
    nombre: str
    capacidad: int

class Cliente(BaseModel):
    nombre: str
    mu: float """

@app.get('/')
def index():
    return 'ayuda'


@app.post('/colas')
def colas(data: Body):
    simu = Simulacion(data.servidores, data.tasa_llegada, data.tasa_servicio)
    simu.empezar()
    tiempo_promedio = simu.get_tiempo_promedio()
    utilizacion = simu.get_utilizacion()
    return {'TiempoPromedio': tiempo_promedio, 'Utilizacion': utilizacion}
    #crear_simulacion = Simulacion()

@app.get('/redes')
def redes():
    sim = Interconexion()
    sim.ejecutar_simulacion()
    cliente = sim.calcular_probabilidad()
    #env.run()
    return {'tiempo': cliente}