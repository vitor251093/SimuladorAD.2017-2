from controllers.agendador import *
from models.cliente import *
from models.fila import *
from random import expovariate
from timeit import Timer
import time

class Simulacao(object):

    def __init__(self):
        self.__momentoDeInicio = time.time()
        self.__clienteDemonstracao = Cliente()

    def tempoAtual(self):
        return time.time()

    def tempoDeSimulacao(self):
        return self.tempoAtual() - self.__momentoDeInicio

    def clienteEntraNaFila(self):
        print "Cliente 1 chegou na fila em: %f" % (self.tempoDeSimulacao())
        t = Timer('self.__clienteDemonstracao.getTempoServico1()', 'from __main__ import self', self.clienteChegaNoServico())
        
    def clienteChegaNoServico(self):
        print "Cliente 1 partiu da fila em: %f" % (self.tempoDeSimulacao())

    def run(self):
        lambd = 0.1
        tempo_de_servico = 1.0
        numero_de_clientes = 99

        agendador = Agendador()
        #fila1 = Fila(1)

        tempo_de_chegada     = agendador.agendarChegadaFila1(self.tempoAtual(), lambd)
        tempo_de_atendimento = agendador.agendarAtendimentoFila1(self.tempoAtual(), tempo_de_servico)
        
        self.__clienteDemonstracao.setID(0)
        self.__clienteDemonstracao.setTempoChegadaFila1(tempo_de_chegada)
        self.__clienteDemonstracao.setTempoServico1(tempo_de_atendimento)

        t = Timer('self.__clienteDemonstracao.getTempoChegadaFila1()', 'from __main__ import self', self.clienteEntraNaFila())


if __name__ == "__main__":
    Simulacao().run()
