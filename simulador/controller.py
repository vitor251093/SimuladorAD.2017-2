from models.cliente import *
from models.fila import *
from models.simulacao import *
from models.agendador import *
from random import expovariate


def rodar():

    lambd = 0.1
    tempo_de_servico = 1.0

    simulacao = Simulacao()
    agendador = Agendador()

    # Agendar primeira chegada
    tempo_de_chegada = agendador.agendarChegadaFila1(simulacao.getTempo(), lambd)
    c = Cliente()
    c.setID(0)
    c.setTempoChegadaFila1(tempo_de_chegada)

    print c.getTempoChegadaFila1()


if __name__ == "__main__":
    rodar()