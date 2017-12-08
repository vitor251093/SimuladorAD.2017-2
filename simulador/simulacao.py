from controllers.agendador import *
from models.cliente import *
from models.fila import *
import random
import math

""" Principal classe do simulador. Simulacao possui o metodo run que inicia todo o processo. """

class Simulacao(object):

    def __init__(self):
        self.__mi = 1
        self.__lambd = 0.3
        self.__numero_de_clientes = 100000
        self.__diferencaAceitavelDasVariancias = 0.0000002
        self.__numero_de_clientes_por_fase = 1000
        
        self.__agendador = Agendador()
        
        self.__clientes = []
        self.__fila1 = Fila(1)
        self.__fila2 = Fila(2)
        
        self.__tempoAtual = 0.0
        self.__indice_cliente_atual = 0
        self.__indice_primeiro_cliente_nao_transiente = 0
        self.__faseTransienteFinalizada = False

        ### Codigo dos principais eventos da simulacao:
        # 0: Evento chegada de Cliente na Fila 1
        # 1: Evento fim de servico 1
        # 2: Evento fim de servico 2
        self.__timerChegadaClienteFila1Indice = 0
        self.__timerFimDeServicoClienteFila1Indice = 1
        self.__timerFimDeServicoClienteFila2Indice = 2

        ### Todos iniciam com valores invalidos: -1
        self.__timerChegadaClienteFila1 = -1
        self.__timerFimDeServicoClienteFila1 = -1
        self.__timerFimDeServicoClienteFila2 = -1

        ### Atributos usados para calculos estatisticos
        self.__somatorioPessoasFila1PorTempo = 0
        self.__somatorioPessoasFilaEspera1PorTempo = 0
        self.__somatorioPessoasFila2PorTempo = 0
        self.__somatorioPessoasFilaEspera2PorTempo = 0

        self.__quantidadeDeEventosPorVariancia = 1000
        self.__eventosDaVariancia1 = []
        self.__duracaoEventosDaVariancia1 = []
        self.__eventosDaVariancia2 = []
        self.__duracaoEventosDaVariancia2 = []

    """ Esse metodo apenas fica responsavel por relizar os somatorios
        para calculo do numero medio de pessoas nas duas filas. """
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
        #print "%f: Cliente %d (%d) %s na fila %d" % (momento, cliente.getID(), cliente.getIndiceDaCor(), evento, fila)
        
        ENt = (self.__somatorioPessoasFila1PorTempo + self.__somatorioPessoasFila2PorTempo)/momento
        print "%f" % (ENt)

        if len(self.__eventosDaVariancia1) < self.__quantidadeDeEventosPorVariancia:
            self.__eventosDaVariancia1.append(ENt)
            self.__duracaoEventosDaVariancia1.append(momento)

        else: 
            if len(self.__eventosDaVariancia2) < self.__quantidadeDeEventosPorVariancia:
                self.__eventosDaVariancia2.append(ENt)
                self.__duracaoEventosDaVariancia2.append(momento)

                if len(self.__eventosDaVariancia2) == self.__quantidadeDeEventosPorVariancia:
                    media1 = 0
                    media2 = 0
                    duracao1 = 0
                    duracao2 = 0
                    for indiceEvento in range(self.__quantidadeDeEventosPorVariancia):
                        media1 += self.__eventosDaVariancia1[indiceEvento]*self.__duracaoEventosDaVariancia1[indiceEvento]
                        media2 += self.__eventosDaVariancia2[indiceEvento]*self.__duracaoEventosDaVariancia2[indiceEvento]
                        duracao1 += self.__duracaoEventosDaVariancia1[indiceEvento]
                        duracao2 += self.__duracaoEventosDaVariancia2[indiceEvento]
                    media1 /= duracao1
                    media2 /= duracao2
                    
                    variancia1 = 0
                    variancia2 = 0
                    for indiceEvento in range(self.__quantidadeDeEventosPorVariancia):
                        variancia1 += (self.__eventosDaVariancia1[indiceEvento] - media1)**2
                        variancia2 += (self.__eventosDaVariancia2[indiceEvento] - media2)**2
                    variancia1 /= (self.__quantidadeDeEventosPorVariancia - 1)
                    variancia2 /= (self.__quantidadeDeEventosPorVariancia - 1)

                    if abs(variancia1 - variancia2) < self.__diferencaAceitavelDasVariancias:
                        self.__faseTransienteFinalizada = True
                    else:
                        self.__eventosDaVariancia1 = self.__eventosDaVariancia2
                        self.__duracaoEventosDaVariancia1 = self.__duracaoEventosDaVariancia2
                        self.__eventosDaVariancia2 = []
                        self.__duracaoEventosDaVariancia2 = []

        return

    def clienteEntraNaFila1 (self):
        self.__indice_cliente_atual += 1
        if self.__faseTransienteFinalizada == True and self.__indice_primeiro_cliente_nao_transiente == 0:
            self.__indice_primeiro_cliente_nao_transiente = self.__indice_cliente_atual

        if self.__indice_primeiro_cliente_nao_transiente == 0:
            corDoCliente = -1
        else:
            corDoCliente = (self.__indice_cliente_atual - self.__indice_primeiro_cliente_nao_transiente)/self.__numero_de_clientes_por_fase

        cliente = Cliente(self.__indice_cliente_atual, self.__tempoAtual, corDoCliente)
        
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

    """ eventoDeDuracaoMinima() ira cuidar da verificacao de qual evento ocorre antes.
        Temos 3 eventos principais: tempo de chegada na fila 1, fim de servico 1 e
        fim de servico 2. Aqui verificamos qual acontece antes. """

    def eventoDeDuracaoMinima(self):

        """ Esse metodo avalia qual o proximo evento em que o simulador deve 
            "entrar" baseado naquele que levara menos tempo para ocorrer no 
            instante atual. """


        # Aqui avaliamos quais dos tres principais eventos da simulacao estao agendados:
        # timerValido1, timerValido2 e timerValido3.

        # Quer dizer que o evento chegada de cliente na fila 1 esta agendado.
        timerValido1 = (self.__timerChegadaClienteFila1      != -1)

        # Quer dizer que o evento fim do servico 1 esta agendado.
        timerValido2 = (self.__timerFimDeServicoClienteFila1 != -1)

        # Quer dizer que o evento fim do servico 2 esta agendado.
        timerValido3 = (self.__timerFimDeServicoClienteFila2 != -1)


        # Essa eh apenas uma condicional para a unica condicao inexperada:
        # a de que nenhuma acao esteja agendada para acontecer;
        # Esse caso so pode ocorrer se houver uma falha do programa,
        # ja que ele deve ser interrompido logo antes disso ocorrer
        if timerValido1 == False and timerValido2 == False and timerValido3 == False:
            return -1


        # As proximas tres condicoes remetem aos casos em que apenas um dos tres
        # eventos esta agendado para ocorrer, entao nao eh necessario
        # compara-los para ver qual ocorrera primeiro:

        # Se nenhuma chegada ira ocorrer e nao ha um cliente da fila 1 sendo
        # atendidos no momento, quer dizer que o proximo evento eh finalizar o 
        # servico de um cliente da fila 2. 
        if timerValido1 == False and timerValido2 == False:
            return self.__timerFimDeServicoClienteFila2Indice

        # Se nenhuma chegada ira ocorrer e nao ha um cliente da fila 2 sendo
        # atendido no momento, quer dizer que o proximo evento eh o fim 
        # do servico de um cliente da fila 1.
        if timerValido1 == False and timerValido3 == False:
            return self.__timerFimDeServicoClienteFila1Indice

        # Se nao ha pessoas da fila 1 nem da fila 2 sendo atendidos,
        # entao o proximo evento eh a chegada de alguem no sistema.
        if timerValido2 == False and timerValido3 == False:
            return self.__timerChegadaClienteFila1Indice


        # As proximas tres condicoes remetem aos casos em que apenas dois dos tres
        # eventos estao agendados para ocorrer, entao so eh necessario comparar
        # esses dois para ver qual ocorrera primeiro:

        # Considerando que ninguem entrara no sistema: O fim de servico de um cliente 
        # da fila 1 ou o fim de servico de um cliente da fila 2 devera acontecer, dependendo
        # de qual dos dois ocorrera em um tempo menor.
        if timerValido1 == False:
            return self.__timerFimDeServicoClienteFila1Indice if self.__timerFimDeServicoClienteFila1 <= self.__timerFimDeServicoClienteFila2 else self.__timerFimDeServicoClienteFila2Indice

        # Considerando que nao ha cliente sendo atendido na fila 1: um cliente entrara
        # no sistema ou o fim de servico de um cliente da fila 2 devera acontecer, dependendo
        # de qual dos dois ocorrera em um tempo menor.
        if timerValido2 == False:
            return self.__timerChegadaClienteFila1Indice if self.__timerChegadaClienteFila1 <= self.__timerFimDeServicoClienteFila2 else self.__timerFimDeServicoClienteFila2Indice

        # Considerando que nao ha cliente sendo atendido na fila 2: um cliente entrara
        # no sistema ou o fim de servico de um cliente da fila 1 devera acontecer, dependendo
        # de qual dos dois ocorrera em um tempo menor.
        if timerValido3 == False:
            return self.__timerChegadaClienteFila1Indice if self.__timerChegadaClienteFila1 <= self.__timerFimDeServicoClienteFila1 else self.__timerFimDeServicoClienteFila1Indice

        
        # A proxima condicao remete ao caso em que os tres eventos estao agendados 
        # para ocorrer, entao eh necessario comparar os tres para ver qual ocorrera primeiro:
        
        # Eh criada uma lista com o tempo que falta ate que cada um dos tres eventos 
        # principais agendados ocorra, ordenados em eventos 0, 1 e 2, posicionados
        # nos respectivos indices da lista
        lista = [self.__timerChegadaClienteFila1, self.__timerFimDeServicoClienteFila1, self.__timerFimDeServicoClienteFila2]

        # Com min(lista), retornamos o menor dos tres tempos presentes na lista;
        # com lista.index(), retornamos o indice desse tempo na lista, conseguindo assim 
        # saber qual o evento com o menor tempo faltante para ocorrer
        return lista.index(min(lista))


    """ O metodo executarProximoEvento(), como o proprio nome diz, executa o proximo evento,
        com base no que foi "decidido" no metodo eventoDeDuracaoMinima(). """
    def executarProximoEvento(self):

        proximoTimer = self.eventoDeDuracaoMinima()

        # Tres eventos principais, tres ifs principais.
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
        

    """ Principal metodo da classe Simulacao. Aqui inicio toda a simulacao. """
    def executarSimulacao(self, seed):
        self.__agendador.configurarSemente(seed)

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


def randomNumber():
    return random.random()

def randomNumberDistantFrom(numbersList, distance):
    newNumber = 0
    while newNumber == 0:
        newNumber = randomNumber()
        for number in numbersList:
            if abs(newNumber - number) < distance:
                newNumber = 0
    return newNumber

if __name__ == "__main__":
    numberOfSimulations = 1
    seedsDistance = 0.01

    numbersList = []

    for i in range(numberOfSimulations):
        newSeed = randomNumberDistantFrom(numbersList, seedsDistance)
        Simulacao().executarSimulacao(newSeed)
        numbersList.append(newSeed)
