from controllers.agendador import *
from models.cliente import *
from models.fila import *
from random import expovariate

class Simulacao(object):

    def __init__(self):
        self.__agendador = Agendador()
        self.__lambd = 0.1

        self.__fila1 = Fila(1)
        #self.__fila2 = Fila(2)
        
        self.__timerChegadaClienteFila1Indice = 0
        self.__timerFimDeServicoClienteFila1Indice = 1
        self.__timerFimDeServicoClienteFila2Indice = 2

        self.__timerChegadaClienteFila1 = -1
        self.__timerFimDeServicoClienteFila1 = -1
        self.__timerFimDeServicoClienteFila2 = -1

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


    def eventoDeDuracaoMinima(self):
        timerValido1 = (self.__timerChegadaClienteFila1      != -1)
        timerValido2 = (self.__timerFimDeServicoClienteFila1 != -1)
        timerValido3 = (self.__timerFimDeServicoClienteFila2 != -1)

        if timerValido1 == False and timerValido2 == False:
            return self.__timerFimDeServicoClienteFila2Indice

        if timerValido1 == False and timerValido3 == False:
            return self.__timerFimDeServicoClienteFila1Indice

        if timerValido2 == False and timerValido3 == False:
            return self.__timerChegadaClienteFila1Indice

        if timerValido1 == False:
            return self.__timerFimDeServicoClienteFila1Indice if self.__timerFimDeServicoClienteFila1 <= self.__timerFimDeServicoClienteFila2 else self.__timerFimDeServicoClienteFila2Indice

        if timerValido2 == False:
            return self.__timerChegadaClienteFila1Indice if self.__timerChegadaClienteFila1 <= self.__timerFimDeServicoClienteFila2 else self.__timerFimDeServicoClienteFila2Indice

        if timerValido3 == False:
            return self.__timerChegadaClienteFila1Indice if self.__timerChegadaClienteFila1 <= self.__timerFimDeServicoClienteFila1 else self.__timerFimDeServicoClienteFila1Indice

        lista = [self.__timerChegadaClienteFila1, self.__timerFimDeServicoClienteFila1, self.__timerFimDeServicoClienteFila2]
        return lista.index(min(lista))

    def executarProximoEvento(self):
        proximoTimer = self.eventoDeDuracaoMinima()
        if proximoTimer == self.__timerChegadaClienteFila1Indice:
            self.__timerFimDeServicoClienteFila1 -= self.__timerChegadaClienteFila1
            self.__timerFimDeServicoClienteFila2 -= self.__timerChegadaClienteFila1
            self.__timerChegadaClienteFila1 = self.__agendador.agendarChegadaFila1(self.__lambd)


        if proximoTimer == self.__timerFimDeServicoClienteFila1Indice:
            self.__timerChegadaClienteFila1      -= self.__timerFimDeServicoClienteFila1
            self.__timerFimDeServicoClienteFila2 -= self.__timerFimDeServicoClienteFila1
            self.__timerFimDeServicoClienteFila1 = self.__agendador.agendarChegadaFila1(self.__lambd)
            

        if proximoTimer == self.__timerFimDeServicoClienteFila2Indice:
            self.__timerChegadaClienteFila1      -= self.__timerFimDeServicoClienteFila2
            self.__timerFimDeServicoClienteFila1 -= self.__timerFimDeServicoClienteFila2
            self.__timerFimDeServicoClienteFila2 = self.__agendador.agendarChegadaFila1(self.__lambd)            

        

    def run(self):
        """lambd = 0.1
        tempo_de_servico = 1.0
        numero_de_clientes = 99

        
        
        tempo_de_chegada     = agendador.agendarChegadaFila1(self.tempoAtual(), lambd)
        tempo_de_atendimento = agendador.agendarAtendimentoFila1(self.tempoAtual(), tempo_de_servico)
        
        clienteDemonstracao = Cliente()
        clienteDemonstracao.setID(1)
        clienteDemonstracao.setTempoChegadaFila1(tempo_de_chegada)
        clienteDemonstracao.setTempoServico1(tempo_de_atendimento)

        self.clienteEntraNoSistema(clienteDemonstracao)"""




if __name__ == "__main__":
    Simulacao().run()
