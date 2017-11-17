from controllers.agendador import *
from models.cliente import *
from models.fila import *
from random import expovariate
from timeit import Timer
import time

class Simulacao(object):

    def __init__(self):
        self.__momentoDeInicio = time.time()
        self.__fila1 = Fila(1)
        #self.__fila2 = Fila(2)
        self.__timerFila1 = None
        #self.__timerFila2 = None

    def tempoAtual(self):
        return time.time()

    def tempoDeSimulacao(self):
        return self.tempoAtual() - self.__momentoDeInicio

    def timerDeCliente(self, funcaoTempo, funcaoExecucao, *args):
        return Timer(('cliente.%s' % (funcaoTempo)), 'from __main__ import cliente', funcaoExecucao(*args))


    def clienteEntraNaFila1(self, cliente):
        self.__fila1.adicionarClienteAFila(cliente)
        print "Cliente %d chegou na fila em: %f" % (cliente.getID(), self.tempoDeSimulacao())
        if self.__fila1.numeroDePessoasNaFila() == 1:
            self.clienteComecaASerAtendidoNaFila1(cliente)
        
    def clienteComecaASerAtendidoNaFila1(self, cliente):
        print "Cliente %d foi atendido em: %f" % (cliente.getID(), self.tempoDeSimulacao())
        self.__timerFila1 = self.timerDeCliente('getTempoServico1()', self.clienteChegaNoServicoNaFila1, cliente)

    def clienteChegaNoServicoNaFila1(self, cliente):
        self.__fila1.retirarClienteEmAtendimento()
        print "Cliente %d terminou o atendimento em: %f" % (cliente.getID(), self.tempoDeSimulacao())
        if self.__fila1.numeroDePessoasNaFila() > 0:
            proximoCliente = self.__fila1.clienteEmAtendimento()
            self.clienteComecaASerAtendidoNaFila1(proximoCliente)

    def clienteEntraNoSistema(self, cliente):
        self.timerDeCliente('getTempoChegadaFila1()', self.clienteEntraNaFila1, cliente)


    def run(self):
        lambd = 0.1
        tempo_de_servico = 1.0
        numero_de_clientes = 99

        agendador = Agendador()
        
        tempo_de_chegada     = agendador.agendarChegadaFila1(self.tempoAtual(), lambd)
        tempo_de_atendimento = agendador.agendarAtendimentoFila1(self.tempoAtual(), tempo_de_servico)
        
        clienteDemonstracao = Cliente()
        clienteDemonstracao.setID(1)
        clienteDemonstracao.setTempoChegadaFila1(tempo_de_chegada)
        clienteDemonstracao.setTempoServico1(tempo_de_atendimento)

        self.clienteEntraNoSistema(clienteDemonstracao)


if __name__ == "__main__":
    Simulacao().run()
