from controllers.agendador import *
from models.cliente import *
from models.fila import *
from random import expovariate

class Simulacao(object):

    def __init__(self):
        self.__agendador = Agendador()
        self.__lambd = -1
        self.__mi = -1

        self.__fila1 = Fila(1)
        self.__fila2 = Fila(2)
        
        self.__tempoAtual = 0.0
        self.__numero_de_clientes = 0
        self.__indice_proximo_cliente = 1

        self.__timerChegadaClienteFila1Indice = 0
        self.__timerFimDeServicoClienteFila1Indice = 1
        self.__timerFimDeServicoClienteFila2Indice = 2

        self.__timerChegadaClienteFila1 = -1
        self.__timerFimDeServicoClienteFila1 = -1
        self.__timerFimDeServicoClienteFila2 = -1


    def clienteEntraNaFila1(self):
        cliente = Cliente(self.__indice_proximo_cliente, self.__tempoAtual)
        self.__indice_proximo_cliente += 1

        self.__fila1.adicionarClienteAFila(cliente)
        print "Cliente %d chegou na fila 1 em: %f" % (cliente.getID(), self.__tempoAtual)
        if self.__fila1.numeroDePessoasNaFila() == 1:
            if self.__fila2.numeroDePessoasNaFila() > 0: # Interrompe individuo da fila 2
                clienteInterrompido = self.__fila2.clienteEmAtendimento()
                clienteInterrompido.setTempoDecorridoServico2(clienteInterrompido.getTempoServico2() - self.__timerFimDeServicoClienteFila2)
                self.__timerFimDeServicoClienteFila2 = -1
            cliente.setTempoChegadaServico1(self.__tempoAtual)
            print "Cliente %d comecou a ser atendido na fila 1 em: %f" % (cliente.getID(), self.__tempoAtual)

            self.__timerFimDeServicoClienteFila1 = self.__agendador.agendarTempoDeServicoFila1(self.__mi)
            cliente.setTempoServico1(self.__timerFimDeServicoClienteFila1)
        
        self.__numero_de_clientes -= 1
        if self.__numero_de_clientes == 0:
            self.__timerChegadaClienteFila1 = -1
        else:    
            self.__timerChegadaClienteFila1 = self.__agendador.agendarChegadaFila1(self.__lambd)
        
        
    def clienteTerminaServicoNaFila1(self):
        cliente = self.__fila1.retirarClienteEmAtendimento()
        print "Cliente %d terminou o atendimento na fila 1 em: %f" % (cliente.getID(), self.__tempoAtual)
        
        self.__fila2.adicionarClienteAFila(cliente)
        cliente.setTempoChegadaFila2(self.__tempoAtual)
        print "Cliente %d chegou na fila 2 em: %f" % (cliente.getID(), self.__tempoAtual)

        if self.__fila1.numeroDePessoasNaFila() > 0:
            novoCliente = self.__fila1.clienteEmAtendimento()
            novoCliente.setTempoChegadaServico1(self.__tempoAtual)
            print "Cliente %d comecou a ser atendido na fila 1 em: %f" % (novoCliente.getID(), self.__tempoAtual)

            self.__timerFimDeServicoClienteFila1 = self.__agendador.agendarTempoDeServicoFila1(self.__mi)
            novoCliente.setTempoServico1(self.__timerFimDeServicoClienteFila1)
        else:
            self.__timerFimDeServicoClienteFila1 = -1
            proximoCliente = self.__fila2.clienteEmAtendimento()
            if proximoCliente.getTempoDecorridoServico2() > 0: # Cliente que foi interrompido
                self.__timerFimDeServicoClienteFila2 = proximoCliente.getTempoServico2() - proximoCliente.getTempoDecorridoServico2()
            else: # Proximo cliente da fila
                proximoCliente.setTempoChegadaServico2(self.__tempoAtual)
                print "Cliente %d comecou a ser atendido na fila 2 em: %f" % (proximoCliente.getID(), self.__tempoAtual)

                self.__timerFimDeServicoClienteFila2 = self.__agendador.agendarTempoDeServicoFila2(self.__mi)
                proximoCliente.setTempoServico2(self.__timerFimDeServicoClienteFila2)

    def clienteTerminaServicoNaFila2(self):
        cliente = self.__fila2.retirarClienteEmAtendimento()
        print "Cliente %d terminou o atendimento na fila 2 em: %f" % (cliente.getID(), self.__tempoAtual)
        if self.__fila2.numeroDePessoasNaFila() > 0:
            proximoCliente = self.__fila2.clienteEmAtendimento()
            proximoCliente.setTempoChegadaServico2(self.__tempoAtual)
            print "Cliente %d comecou a ser atendido na fila 2 em: %f" % (proximoCliente.getID(), self.__tempoAtual)

            self.__timerFimDeServicoClienteFila2 = self.__agendador.agendarTempoDeServicoFila2(self.__mi)
            proximoCliente.setTempoServico2(self.__timerFimDeServicoClienteFila2)
        else:
            self.__timerFimDeServicoClienteFila2 = -1


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
            self.__tempoAtual += self.__timerChegadaClienteFila1
            if self.__timerFimDeServicoClienteFila1 != -1:
                self.__timerFimDeServicoClienteFila1 -= self.__timerChegadaClienteFila1
            if self.__timerFimDeServicoClienteFila2 != -1:
                self.__timerFimDeServicoClienteFila2 -= self.__timerChegadaClienteFila1
            self.clienteEntraNaFila1()

        if proximoTimer == self.__timerFimDeServicoClienteFila1Indice:
            self.__tempoAtual += self.__timerFimDeServicoClienteFila1
            if self.__timerChegadaClienteFila1 != -1:
                self.__timerChegadaClienteFila1 -= self.__timerFimDeServicoClienteFila1
            if self.__timerFimDeServicoClienteFila2 != -1:
                self.__timerFimDeServicoClienteFila2 -= self.__timerFimDeServicoClienteFila1
            self.clienteTerminaServicoNaFila1()

        if proximoTimer == self.__timerFimDeServicoClienteFila2Indice:
            self.__tempoAtual += self.__timerFimDeServicoClienteFila2
            if self.__timerChegadaClienteFila1 != -1:
                self.__timerChegadaClienteFila1 -= self.__timerFimDeServicoClienteFila2
            if self.__timerFimDeServicoClienteFila1 != -1:
                self.__timerFimDeServicoClienteFila1 -= self.__timerFimDeServicoClienteFila2
            self.clienteTerminaServicoNaFila2()
        

    def run(self):
        self.__mi = 0.1
        self.__lambd = 0.1
        self.__numero_de_clientes = 99

        self.__timerChegadaClienteFila1 = self.__agendador.agendarChegadaFila1(self.__lambd)

        while self.__numero_de_clientes > 0 or self.__fila1.numeroDePessoasNaFila() > 0 or self.__fila2.numeroDePessoasNaFila() > 0:
            self.executarProximoEvento()


if __name__ == "__main__":
    Simulacao().run()
