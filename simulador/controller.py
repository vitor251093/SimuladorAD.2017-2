from models.cliente import *
from models.fila import *
from models.simulacao import *
from models.agendador import *
from random import expovariate


def rodar():

    lambd = 0.1
    tempo_de_servico = 1.0
    numero_de_clientes = 99

    simulacao = Simulacao()
    agendador = Agendador()
    fila1 = Fila(1)

    # Agendar primeira chegada
    tempo_de_chegada = agendador.agendarChegadaFila1(simulacao.getTempo(), lambd)
    # O tempo de simulacao "vai" para o tempo do primeiro evento
    simulacao.setTempo(tempo_de_chegada)
    cliente = Cliente()
    cliente.setID(0)
    cliente.setTempoChegadaFila1(tempo_de_chegada)
    cliente.setTempoServico1(tempo_de_servico)

    print "Cliente 1 chegou em: %f" % (cliente.getTempoChegadaFila1())

    tempo_de_partida = agendador.agendarAtendimentoFila1(simulacao.getTempo(), tempo_de_servico)
    simulacao.setTempo(tempo_de_partida)

    print "Cliente 1 parte em: %f" % (simulacao.getTempo())


if __name__ == "__main__":
    rodar()

if __name__ == "__main__":
    rodar()
