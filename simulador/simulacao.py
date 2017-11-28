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

        ### Codigo dos principais eventos da simulacao
        # 0: Evento chegada de Cliente na Fila 1
        # 1: Evento fim de servico 1
        # 2: Evento fim de servico 2
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

    def agregarEmSomatorioPessoasPorTempo (self, tempo):
        self.__somatorioPessoasFila1PorTempo += tempo * (self.__fila1.numeroDePessoasNaFila())
        self.__somatorioPessoasFila2PorTempo += tempo * (self.__fila2.numeroDePessoasNaFila())

        if self.__fila1.numeroDePessoasNaFila() > 0:
            self.__somatorioPessoasFilaEspera1PorTempo += tempo * (self.__fila1.numeroDePessoasNaFila() - 1)

        if self.__fila1.numeroDePessoasNaFila() > 0:
            self.__somatorioPessoasFilaEspera2PorTempo += tempo * (self.__fila2.numeroDePessoasNaFila())
        else:
            if self.__fila2.numeroDePessoasNaFila() > 0:
                self.__somatorioPessoasFilaEspera2PorTempo += tempo * (self.__fila2.numeroDePessoasNaFila() - 1)

    def adicionarEvento (self, cliente, evento, fila, momento):
        print "%f: Cliente %d %s na fila %d" % (momento, cliente.getID(), evento, fila)
        return

    def clienteEntraNaFila1 (self):
        self.__indice_cliente_atual += 1
        cliente = Cliente(self.__indice_cliente_atual, self.__tempoAtual)
        
        self.__clientes.append(cliente)
        self.__fila1.adicionarClienteAFila(cliente)

        self.adicionarEvento(cliente, "chegou", self.__fila1.getID(), self.__tempoAtual)
        if self.__fila1.numeroDePessoasNaFila() == 1:
            if self.__fila2.numeroDePessoasNaFila() > 0: # Interrompe individuo da fila 2
                clienteInterrompido = self.__fila2.clienteEmAtendimento()
                clienteInterrompido.setTempoDecorridoServico2(clienteInterrompido.getTempoServico2() - self.__timerFimDeServicoClienteFila2)
                self.__timerFimDeServicoClienteFila2 = -1
            
            cliente.setTempoChegadaServico1(self.__tempoAtual)
            
            self.__timerFimDeServicoClienteFila1 = self.__agendador.agendarTempoDeServicoFila1(self.__mi)
            cliente.setTempoServico1(self.__timerFimDeServicoClienteFila1)

        if self.__numero_de_clientes - self.__indice_cliente_atual == 0:
            self.__timerChegadaClienteFila1 = -1
        else:    
            self.__timerChegadaClienteFila1 = self.__agendador.agendarChegadaFila1(self.__lambd)


    def clienteTerminaServicoNaFila1(self):
        cliente = self.__fila1.retirarClienteEmAtendimento()
        self.adicionarEvento(cliente, "terminou o atendimento", self.__fila1.getID(), self.__tempoAtual)

        self.__fila2.adicionarClienteAFila(cliente)
        cliente.setTempoChegadaFila2(self.__tempoAtual)
        
        if self.__fila1.numeroDePessoasNaFila() > 0:
            novoCliente = self.__fila1.clienteEmAtendimento()
            novoCliente.setTempoChegadaServico1(self.__tempoAtual)

            self.__timerFimDeServicoClienteFila1 = self.__agendador.agendarTempoDeServicoFila1(self.__mi)
            novoCliente.setTempoServico1(self.__timerFimDeServicoClienteFila1)
        else:
            self.__timerFimDeServicoClienteFila1 = -1
            proximoCliente = self.__fila2.clienteEmAtendimento()
            if proximoCliente.getTempoDecorridoServico2() > 0: # Cliente que foi interrompido
                self.__timerFimDeServicoClienteFila2 = proximoCliente.getTempoServico2() - proximoCliente.getTempoDecorridoServico2()
                
            else: # Proximo cliente da fila
                self.__timerFimDeServicoClienteFila2 = self.__agendador.agendarTempoDeServicoFila2(self.__mi)
                proximoCliente.setTempoServico2(self.__timerFimDeServicoClienteFila2)

    def clienteTerminaServicoNaFila2(self):
        cliente = self.__fila2.retirarClienteEmAtendimento()
        cliente.setTempoTerminoServico2(self.__tempoAtual)

        self.adicionarEvento(cliente, "terminou o atendimento", self.__fila2.getID(), self.__tempoAtual)
        if self.__fila2.numeroDePessoasNaFila() > 0:
            proximoCliente = self.__fila2.clienteEmAtendimento()
            
            self.__timerFimDeServicoClienteFila2 = self.__agendador.agendarTempoDeServicoFila2(self.__mi)
            proximoCliente.setTempoServico2(self.__timerFimDeServicoClienteFila2)
        else:
            self.__timerFimDeServicoClienteFila2 = -1


    def eventoDeDuracaoMinima(self):

        """ Esse metodo faz o simulador "entrar" nos eventos corretos
            de acordo com uma serie de condicoes explicitadas abaixo.
            Tambem verifica quais dos tres principais eventos ocorre antes. """


        # Aqui marco os acontecimentos dos tres principais eventos da Simulacao:
        # timerValido1, timerValido2 e timerValido3.


        # Quer dizer que o evento chegada de cliente na fila 1 ocorreu.
        timerValido1 = (self.__timerChegadaClienteFila1      != -1)


        # Quer dizer que o evento fim do servico 1 ocorreu.
        timerValido2 = (self.__timerFimDeServicoClienteFila1 != -1)


        # Quer dizer que o evento fim do servico 2 ocorreu.
        timerValido3 = (self.__timerFimDeServicoClienteFila2 != -1)


        # Se nao ocorreu chegada alguma e tambem nao ocorreu nenhum fim de servico 1,
        # isso quer dizer que o proximo evento eh finalizar o fim de servico 2.
        # Aqui atendo clientes da fila 2 ate chegar alguem na fila 1.
        if timerValido1 == False and timerValido2 == False:
            return self.__timerFimDeServicoClienteFila2Indice

        # Se nao ocorreu nenhuma chegada na Fila 1 e nao ocorreu nenhum fim de servico 2,
        # isso quer dizer que existia alguem recebendo o servico 1 e o proximo evento e finalizar seu servico.
        if timerValido1 == False and timerValido3 == False:
            return self.__timerFimDeServicoClienteFila1Indice

        # Se nao teve fim de servico 1 e nem fim de servico 2,
        # isso quer dizer que o proximo evento e a chegada de alguem na fila 1.
        if timerValido2 == False and timerValido3 == False:
            return self.__timerChegadaClienteFila1Indice

        # Retorno 0 caso o evento fim de servico 1 aconteca antes de todos.
        # Retorno 2 caso contrario, pois como timerValido1 eh False, significa que nao houve chegada na Fila 1
        if timerValido1 == False:
            return self.__timerFimDeServicoClienteFila1Indice if self.__timerFimDeServicoClienteFila1 <= self.__timerFimDeServicoClienteFila2 else self.__timerFimDeServicoClienteFila2Indice

        # Como timerValido2 eh False, sei que nao houve fim do servico 1 de algum Cliente.
        # Retorno 1 caso o evento chegada de Cliente na Fila 1 aconteca antes.
        # Retorno 2 caso contrario, o que significa que houve um fim de um servico 2.
        if timerValido2 == False:
            return self.__timerChegadaClienteFila1Indice if self.__timerChegadaClienteFila1 <= self.__timerFimDeServicoClienteFila2 else self.__timerFimDeServicoClienteFila2Indice

        # Como timerValido3 eh False, sei que nao houve fim de um servico 2.
        # Retorno 0 caso o evento chegada Cliente na Fila 1 aconteca antes.
        # Retorno 1 caso contrario, o que significa que houve um fim de servico 1.
        if timerValido3 == False:
            return self.__timerChegadaClienteFila1Indice if self.__timerChegadaClienteFila1 <= self.__timerFimDeServicoClienteFila1 else self.__timerFimDeServicoClienteFila1Indice

        # A lista de tempos dos tres eventos que ocorrem durante o tempo de simulacao.
        lista = [self.__timerChegadaClienteFila1, self.__timerFimDeServicoClienteFila1, self.__timerFimDeServicoClienteFila2]

        # Retorno o menor, ou seja, o que ocorreu antes.
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

        """"""

        # Comeco agendando a chegada do primeiro Cliente no sistema.
        # A partir dela os proximo eventos sao gerados no loop principal da simulacao (mais abaixo).
        self.__timerChegadaClienteFila1 = self.__agendador.agendarChegadaFila1(self.__lambd)


        # Loop principal da simulacao
        while self.__numero_de_clientes > self.__indice_cliente_atual or self.__fila1.numeroDePessoasNaFila() > 0 or self.__fila2.numeroDePessoasNaFila() > 0:
            self.executarProximoEvento()


        # Calculo de estatisticas da simulacao
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


        # Impressao dos resultados das estatisticas
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
