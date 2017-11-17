from controllers.agendador import *
from models.cliente import *
from models.fila import *
from random import expovariate

class Simulacao(object):

    def __init__(self):
        self.__numero_de_clientes = 100
        self.__lambd = 1.0

    def run(self):
        pass

if __name__ == "__main__":
    Simulacao().run()
