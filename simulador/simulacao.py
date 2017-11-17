from controllers.agendador import *
from models.cliente import *
from models.fila import *
from random import expovariate
from timeit import Timer
import time

class Simulacao(object):

    def __init__(self):
        self.__momentoDeInicio = time.time()

    def tempoAtual(self):
        return time.time()

    def tempoDeSimulacao(self):
        return self.tempoAtual() - self.__momentoDeInicio

    def clienteEntraNaFila(self, cliente):
        print "Cliente %d chegou na fila em: %f" % (cliente.getID(), self.tempoDeSimulacao())
        t = Timer('cliente.getTempoServico1()', 'from __main__ import cliente', self.clienteChegaNoServico(cliente))
        
    def clienteChegaNoServico(self, cliente):
        print "Cliente %d partiu da fila em: %f" % (cliente.getID(), self.tempoDeSimulacao())

    def clienteEntraNoSistema(self, cliente):
        t = Timer('cliente.getTempoChegadaFila1()', 'from __main__ import cliente', self.clienteEntraNaFila(cliente))

    def run(self):
        lambd = 0.1
        tempo_de_servico = 1.0
        numero_de_clientes = 99

        agendador = Agendador()
        #fila1 = Fila(1)

        tempo_de_chegada     = agendador.agendarChegadaFila1(self.tempoAtual(), lambd)
        tempo_de_atendimento = agendador.agendarAtendimentoFila1(self.tempoAtual(), tempo_de_servico)
        
        clienteDemonstracao = Cliente()
        clienteDemonstracao.setID(1)
        clienteDemonstracao.setTempoChegadaFila1(tempo_de_chegada)
        clienteDemonstracao.setTempoServico1(tempo_de_atendimento)

        self.clienteEntraNoSistema(clienteDemonstracao)


if __name__ == "__main__":
    Simulacao().run()
