from controllers.agendador import *
from models.cliente import *
from models.fila import *

class Simulacao(object):

    def __init__(self):
        self.__mi = 1
        self.__lambd = 0.4995
        self.__numero_de_clientes = 1000000

        
        self.__agendador = Agendador()
        
        self.__clientes = []
        self.__fila1 = Fila(1)
        self.__fila2 = Fila(2)
        
        self.__tempoAtual = 0.0
        self.__indice_cliente_atual = 0

        self.__timerChegadaClienteFila1Indice = 0
        self.__timerFimDeServicoClienteFila1Indice = 1
        self.__timerFimDeServicoClienteFila2Indice = 2

        self.__timerChegadaClienteFila1 = -1
        self.__timerFimDeServicoClienteFila1 = -1
        self.__timerFimDeServicoClienteFila2 = -1

        self.__somatorioPessoasFila1PorTempo = 0
        self.__somatorioPessoasFilaEspera1PorTempo = 0
        self.__somatorioPessoasFila2PorTempo = 0
        self.__somatorioPessoasFilaEspera2PorTempo = 0

    def agregarEmSomatorioPessoasPorTempo(self, tempo):
        self.__somatorioPessoasFila1PorTempo += tempo * (self.__fila1.numeroDePessoasNaFila())
        self.__somatorioPessoasFila2PorTempo += tempo * (self.__fila2.numeroDePessoasNaFila())

        if self.__fila1.numeroDePessoasNaFila() > 0:
            self.__somatorioPessoasFilaEspera1PorTempo += tempo * (self.__fila1.numeroDePessoasNaFila() - 1)

        if self.__fila1.numeroDePessoasNaFila() > 0:
            self.__somatorioPessoasFilaEspera2PorTempo += tempo * (self.__fila2.numeroDePessoasNaFila())
        else:
            if self.__fila2.numeroDePessoasNaFila() > 0:
                self.__somatorioPessoasFilaEspera2PorTempo += tempo * (self.__fila2.numeroDePessoasNaFila() - 1)

    def clienteEntraNaFila1(self):
        self.__indice_cliente_atual += 1
        cliente = Cliente(self.__indice_cliente_atual, self.__tempoAtual)
        
        self.__clientes.append(cliente)
        self.__fila1.adicionarClienteAFila(cliente)

        print "Cliente %d chegou na fila 1 em: %f" % (cliente.getID(), self.__tempoAtual)
        if self.__fila1.numeroDePessoasNaFila() == 1:
            if self.__fila2.numeroDePessoasNaFila() > 0: # Interrompe individuo da fila 2
                clienteInterrompido = self.__fila2.clienteEmAtendimento()
                clienteInterrompido.setTempoDecorridoServico2(clienteInterrompido.getTempoServico2() - self.__timerFimDeServicoClienteFila2)
                self.__timerFimDeServicoClienteFila2 = -1
                print "Cliente %d foi interrompido em: %f" % (clienteInterrompido.getID(), self.__tempoAtual)

            cliente.setTempoChegadaServico1(self.__tempoAtual)
            print "Cliente %d comecou a ser atendido na fila 1 em: %f" % (cliente.getID(), self.__tempoAtual)

            self.__timerFimDeServicoClienteFila1 = self.__agendador.agendarTempoDeServicoFila1(self.__mi)
            cliente.setTempoServico1(self.__timerFimDeServicoClienteFila1)

        if self.__numero_de_clientes - self.__indice_cliente_atual == 0:
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
                print "Cliente %d retomou o atendimento na fila 2 em: %f" % (proximoCliente.getID(), self.__tempoAtual)
            else: # Proximo cliente da fila
                proximoCliente.setTempoChegadaServico2(self.__tempoAtual)
                print "Cliente %d comecou a ser atendido na fila 2 em: %f" % (proximoCliente.getID(), self.__tempoAtual)

                self.__timerFimDeServicoClienteFila2 = self.__agendador.agendarTempoDeServicoFila2(self.__mi)
                proximoCliente.setTempoServico2(self.__timerFimDeServicoClienteFila2)

    def clienteTerminaServicoNaFila2(self):
        cliente = self.__fila2.retirarClienteEmAtendimento()
        cliente.setTempoTerminoServico2(self.__tempoAtual)

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
            self.agregarEmSomatorioPessoasPorTempo(self.__timerChegadaClienteFila1)

            self.__tempoAtual += self.__timerChegadaClienteFila1
            if self.__timerFimDeServicoClienteFila1 != -1:
                self.__timerFimDeServicoClienteFila1 -= self.__timerChegadaClienteFila1
            if self.__timerFimDeServicoClienteFila2 != -1:
                self.__timerFimDeServicoClienteFila2 -= self.__timerChegadaClienteFila1
            self.clienteEntraNaFila1()

        if proximoTimer == self.__timerFimDeServicoClienteFila1Indice:
            self.agregarEmSomatorioPessoasPorTempo(self.__timerFimDeServicoClienteFila1)
            
            self.__tempoAtual += self.__timerFimDeServicoClienteFila1
            if self.__timerChegadaClienteFila1 != -1:
                self.__timerChegadaClienteFila1 -= self.__timerFimDeServicoClienteFila1
            if self.__timerFimDeServicoClienteFila2 != -1:
                self.__timerFimDeServicoClienteFila2 -= self.__timerFimDeServicoClienteFila1
            self.clienteTerminaServicoNaFila1()

        if proximoTimer == self.__timerFimDeServicoClienteFila2Indice:
            self.agregarEmSomatorioPessoasPorTempo(self.__timerFimDeServicoClienteFila2)
            
            self.__tempoAtual += self.__timerFimDeServicoClienteFila2
            if self.__timerChegadaClienteFila1 != -1:
                self.__timerChegadaClienteFila1 -= self.__timerFimDeServicoClienteFila2
            if self.__timerFimDeServicoClienteFila1 != -1:
                self.__timerFimDeServicoClienteFila1 -= self.__timerFimDeServicoClienteFila2
            self.clienteTerminaServicoNaFila2()
        

    def run(self):
        self.__timerChegadaClienteFila1 = self.__agendador.agendarChegadaFila1(self.__lambd)

        while self.__numero_de_clientes > self.__indice_cliente_atual or self.__fila1.numeroDePessoasNaFila() > 0 or self.__fila2.numeroDePessoasNaFila() > 0:
            self.executarProximoEvento()

        somatorioT1 = 0.0
        somatorioW1 = 0.0
        somatorioT2 = 0.0
        somatorioW2 = 0.0
        for cliente in self.__clientes:
            somatorioT1 += cliente.getTempoTotalFila1()
            somatorioW1 += cliente.getTempoEsperaFila1()
            somatorioT2 += cliente.getTempoTotalFila2()
            somatorioW2 += cliente.getTempoEsperaFila2()
        ET1 = somatorioT1/len(self.__clientes)
        EW1 = somatorioW1/len(self.__clientes)
        ET2 = somatorioT2/len(self.__clientes)
        EW2 = somatorioW2/len(self.__clientes)

        somatorioVW1 = 0.0
        somatorioVW2 = 0.0
        for cliente in self.__clientes:
            somatorioVW1 += cliente.getVarianciaTempoEsperaFila1(EW1)
            somatorioVW2 += cliente.getVarianciaTempoEsperaFila2(EW2)
        EVW1 = somatorioVW1/len(self.__clientes)
        EVW2 = somatorioVW2/len(self.__clientes)

        print "E[T1]:  %f" % (ET1)
        print "E[W1]:  %f" % (EW1)
        print "V(W1):  %f" % (EVW1)
        print "E[N1]:  %f" % (self.__somatorioPessoasFila1PorTempo / self.__tempoAtual)
        print "E[Nq1]: %f" % (self.__somatorioPessoasFilaEspera1PorTempo / self.__tempoAtual)
        print "E[T2]:  %f" % (ET2)
        print "E[W2]:  %f" % (EW2)
        print "V(W2):  %f" % (EVW2)
        print "E[N2]:  %f" % (self.__somatorioPessoasFila2PorTempo / self.__tempoAtual)
        print "E[Nq2]: %f" % (self.__somatorioPessoasFilaEspera2PorTempo / self.__tempoAtual)


if __name__ == "__main__":
    Simulacao().run()
