from controllers.agendador import *
from models.cliente import *
from models.fila import *
from models.fase import *
import random
import math
import sys
import getopt
import os
from time import gmtime, strftime

""" Principal classe do simulador. Simulacao possui o metodo run que inicia todo o processo. """

class Simulacao(object):

    def __init__(self):
        self.__mi = None
        self.__lambd = None
        self.__numero_de_clientes_por_fase = None
        self.__numero_de_rodadas = None

        self.__seedsDistance = 0.01
        self.__seedsList = []
        self.__output_file = None
        
        self.__agendador = Agendador()
        
        self.__clientes = []
        self.__fila1 = Fila(1)
        self.__fila2 = Fila(2)
        
        self.__fases = []
        self.__fase = Fase(-1, 0)
        
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

        ### Atributos usados para determinar o fim da fase transiente
        self.__quantidadeDeEventosPorVariancia = 1000
        self.__diferencaAceitavelDasVariancias = 0.0000002
        self.__eventosDaVariancia1 = []
        self.__duracaoEventosDaVariancia1 = []
        self.__eventosDaVariancia2 = []
        self.__duracaoEventosDaVariancia2 = []


    """ Esse metodo apenas fica responsavel por relizar os somatorios
        para o calculo do numero medio de pessoas nas duas filas (E[Ns]). """
    def agregarEmSomatorioPessoasPorTempo (self, tempo):
        self.__fase.inserirNumeroDeClientesPorTempoNaFila1(self.__fila1.numeroDePessoasNaFila(), tempo)
        self.__fase.inserirNumeroDeClientesPorTempoNaFila2(self.__fila1.numeroDePessoasNaFila(), tempo)

        if self.__fila1.numeroDePessoasNaFila() > 0:
            self.__fase.inserirNumeroDeClientesPorTempoNaFilaEspera1(self.__fila1.numeroDePessoasNaFila() - 1, tempo)
        else:
            self.__fase.inserirNumeroDeClientesPorTempoNaFilaEspera1(0, tempo)

        if self.__fila1.numeroDePessoasNaFila() > 0:
            self.__fase.inserirNumeroDeClientesPorTempoNaFilaEspera2(self.__fila2.numeroDePessoasNaFila(), tempo)
        else:
            if self.__fila2.numeroDePessoasNaFila() > 0:
                self.__fase.inserirNumeroDeClientesPorTempoNaFilaEspera2(self.__fila2.numeroDePessoasNaFila() - 1, tempo)
            else: 
                self.__fase.inserirNumeroDeClientesPorTempoNaFilaEspera2(0, tempo)


    def adicionarEvento (self, cliente, evento, fila, momento):
        #print "%f: Cliente %d (%d) %s na fila %d" % (momento, cliente.getID(), cliente.getIndiceDaCor(), evento, fila)
        
        ENt = self.__fase.getEsperancaDeN(momento)

        if self.__output_file == None:
            print "%f,%d" % (ENt, cliente.getIndiceDaCor())
        else:
            self.__output_file.write("%f,%d\n" % (ENt, cliente.getIndiceDaCor()))
        
        if self.__faseTransienteFinalizada == True:
            return

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


    def randomNumber(self):
        return random.random()

    def randomNumberDistantFrom(self, numbersList, distance):
        newNumber = 0
        while newNumber == 0:
            newNumber = self.randomNumber()
            for number in numbersList:
                if abs(newNumber - number) < distance:
                    newNumber = 0
        return newNumber

    def clienteEntraNaFila1 (self):
        self.__indice_cliente_atual += 1
        if self.__faseTransienteFinalizada == True and self.__indice_primeiro_cliente_nao_transiente == 0:
            self.__indice_primeiro_cliente_nao_transiente = self.__indice_cliente_atual

        if self.__indice_primeiro_cliente_nao_transiente == 0:
            corDoCliente = -1
        else:
            indiceDaFase = (self.__indice_cliente_atual - self.__indice_primeiro_cliente_nao_transiente)/self.__numero_de_clientes_por_fase
            if indiceDaFase > self.__fase.getID():
                self.__fase.calcularEstatisticas(self.__tempoAtual - self.__timerChegadaClienteFila1)

                newSeed = self.randomNumberDistantFrom(self.__seedsList, self.__seedsDistance)
                self.__agendador.configurarSemente(newSeed)
                self.__fase = Fase(indiceDaFase, self.__tempoAtual)
            corDoCliente = indiceDaFase

        cliente = Cliente(self.__indice_cliente_atual, self.__tempoAtual, corDoCliente)
        
        self.__fase.adicionarCliente(cliente)
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

        if self.__faseTransienteFinalizada == False:
            self.__timerChegadaClienteFila1 = self.__agendador.agendarChegadaFila1(self.__lambd)
            return

        if self.__fase.getID() + 1 == self.__numero_de_rodadas and self.__fase.quantidadeDeClientes() == self.__numero_de_clientes_por_fase:
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
    def executarSimulacao(self, seed, lambdaValue, miValue, numeroDeClientesPorRodada, rodadas, hasOutputFile, testeDeCorretude):
        self.__lambd = lambdaValue
        self.__mi = miValue
        self.__numero_de_clientes_por_fase = numeroDeClientesPorRodada
        self.__numero_de_rodadas = rodadas

        if hasOutputFile == True:
            dir_path = os.path.dirname(os.path.abspath(__file__))
            file_path = "/../plot/%s.csv" % (strftime("%Y-%m-%d %H.%M.%S", gmtime()))
            self.__output_file = open(dir_path + file_path, "w")

        self.__agendador.setTesteDeCorretude(testeDeCorretude)
        self.__agendador.configurarSemente(seed)

        # Comeco agendando a chegada do primeiro Cliente no sistema.
        # A partir dela os proximo eventos sao gerados no loop principal da simulacao (mais abaixo).
        self.__timerChegadaClienteFila1 = self.__agendador.agendarChegadaFila1(self.__lambd)


        # Loop principal da simulacao
        while self.__numero_de_rodadas > self.__fase.getID() + 1 or self.__numero_de_clientes_por_fase > self.__fase.quantidadeDeClientes() or self.__fila1.numeroDePessoasNaFila() > 0 or self.__fila2.numeroDePessoasNaFila() > 0:
            self.executarProximoEvento()

        if hasOutputFile == True:
            self.__output_file.close() 

        self.__fase.calcularEstatisticas(self.__tempoAtual)
        


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

def printHelp():
    print 'Uso: simulacao.py [args]'
    print 'Opcoes e argumentos:'
    print '-l, --lambda\t\t\tEspecifica o valor de lambda (Padrao: 0.3)'
    print '-m, --mi\t\t\tEspecifica o valor de mi (Padrao: 1.0)'
    print '-c, --clientes-por-rodada\tEspecifica o numero de clientes por rodada (Padrao: 20000)'
    print '-r, --rodadas\t\t\tEspecifica o numero de rodadas (Padrao: 100)'
    print '-s, --simulacoes\t\tEspecifica o numero de simulacoes (Padrao: 1)'
    print '-o, --csv-output\t\tDefine que a saida deve ser em um arquivo csv no diretorio \'plot\''
    print '-t, --teste\t\t\tExecuta o programa em modo de Teste de Corretude'

def safeInt(key, stringValue):
    try:
        return int(stringValue)
    except ValueError:
        print "ERRO: A chave \"%s\" aceita apenas valores inteiros (int)." % (key)
        sys.exit(2)

def safeFloat(key, stringValue):
    try:
        return float(stringValue)
    except ValueError:
        print "ERRO: A chave \"%s\" aceita apenas valores de ponto flutuante (float)." % (key)
        sys.exit(2)

def main(argv):
    lambdaValue = 0.3
    miValue = 1
    numeroDeClientesPorRodada = 20000
    rodadas = 100
    simulacoes = 1
    outputFile = False
    testeDeCorretude = False
    try:
        opts, args = getopt.getopt(argv,"hotl:m:c:r:s",["help","csv-output","teste","lambda=","mi=","clientes-por-rodada=","rodadas=","simulacoes="])
    except getopt.GetoptError:
        printHelp()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            printHelp()
            sys.exit()
        elif opt in ("-l", "--lambda"):
            lambdaValue = safeFloat("lambda",arg)
        elif opt in ("-m", "--mi"):
            miValue = safeFloat("mi",arg)
        elif opt in ("-c", "--clientes-por-rodada"):
            numeroDeClientesPorRodada = safeInt("clientes por rodada",arg)
        elif opt in ("-r", "--rodadas"):
            rodadas = safeInt("rodadas", arg)
        elif opt in ("-s", "--simulacoes"):
            simulacoes = safeInt("simulacoes", arg)
        elif opt in ("-o", "--csv-output"):
            outputFile = True
        elif opt in ("-t", "--teste"):
            testeDeCorretude = True
    
    seedsDistance = 0.01
    seedsList = []

    for i in range(simulacoes):
        newSeed = randomNumberDistantFrom(seedsList, seedsDistance)
        Simulacao().executarSimulacao(newSeed, lambdaValue, miValue, numeroDeClientesPorRodada, rodadas, outputFile, testeDeCorretude)
        seedsList.append(newSeed)

if __name__ == "__main__":
    main(sys.argv[1:])