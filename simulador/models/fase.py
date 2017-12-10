from controllers.calculadora_ic import *

class Fase(object):
    def __init__(self, id, tempoInicial):
        self.__id = id
        self.__clientes = []
        self.__tempoInicial = tempoInicial

        ### Atributos usados para calculos estatisticos
        self.__pessoasFila1PorTempo = []
        self.__pessoasFilaEspera1PorTempo = []
        self.__pessoasFila2PorTempo = []
        self.__pessoasFilaEspera2PorTempo = []
        self.__somatorioPessoasFila1PorTempo = 0
        self.__somatorioPessoasFilaEspera1PorTempo = 0
        self.__somatorioPessoasFila2PorTempo = 0
        self.__somatorioPessoasFilaEspera2PorTempo = 0
        
    def adicionarCliente(self, cliente):
        self.__clientes.append(cliente)

    # Getters
    def getID(self):
        return self.__id

    def quantidadeDeClientes(self):
        return len(self.__clientes)

    def getEsperancaDeN(self, tempoAtual):
        if tempoAtual == self.__tempoInicial:
            return 0
        return (self.__somatorioPessoasFila1PorTempo + self.__somatorioPessoasFila2PorTempo)/(tempoAtual-self.__tempoInicial)

    def inserirNumeroDeClientesPorTempoNaFila1(self, numeroDeClientes, tempo):
        self.__pessoasFila1PorTempo.append(numeroDeClientes)
        self.__somatorioPessoasFila1PorTempo += tempo * numeroDeClientes

    def inserirNumeroDeClientesPorTempoNaFila2(self, numeroDeClientes, tempo):
        self.__pessoasFila2PorTempo.append(numeroDeClientes)
        self.__somatorioPessoasFila2PorTempo += tempo * numeroDeClientes

    def inserirNumeroDeClientesPorTempoNaFilaEspera1(self, numeroDeClientes, tempo):
        self.__pessoasFilaEspera1PorTempo.append(numeroDeClientes)
        self.__somatorioPessoasFilaEspera1PorTempo += tempo * numeroDeClientes

    def inserirNumeroDeClientesPorTempoNaFilaEspera2(self, numeroDeClientes, tempo):
        self.__pessoasFilaEspera2PorTempo.append(numeroDeClientes)
        self.__somatorioPessoasFilaEspera2PorTempo += tempo * numeroDeClientes

    def calcularEstatisticas(self, tempoAtual):
        # Calculo de estatisticas da simulacao
        clientesT1 = []
        clientesW1 = []
        clientesT2 = []
        clientesW2 = []
        somatorioT1 = 0.0
        somatorioW1 = 0.0
        somatorioT2 = 0.0
        somatorioW2 = 0.0
        for cliente in self.__clientes:
            if cliente.getTempoServico1() != 0:
                clientesW1.append(cliente.getTempoEsperaFila1())
                somatorioW1 += cliente.getTempoEsperaFila1()
            
            if cliente.getTempoChegadaFila2() != 0:
                clientesT1.append(cliente.getTempoTotalFila1())
                somatorioT1 += cliente.getTempoTotalFila1()
            
            if cliente.getTempoTerminoServico2() != 0:
                clientesT2.append(cliente.getTempoTotalFila2())
                somatorioT2 += cliente.getTempoTotalFila2()
                
                clientesW2.append(cliente.getTempoEsperaFila2())
                somatorioW2 += cliente.getTempoEsperaFila2()

        ET1 = somatorioT1/len(self.__clientes)
        EW1 = somatorioW1/len(self.__clientes)
        ET2 = somatorioT2/len(self.__clientes)
        EW2 = somatorioW2/len(self.__clientes)

        clientesVW1 = []
        clientesVW2 = []
        somatorioVW1 = 0.0
        somatorioVW2 = 0.0
        for cliente in self.__clientes:
            if cliente.getTempoServico1() != 0:
                clientesVW1.append(cliente.getVarianciaTempoEsperaFila1(EW1))
                somatorioVW1 += cliente.getVarianciaTempoEsperaFila1(EW1)
            
            if cliente.getTempoTerminoServico2() != 0:
                clientesVW2.append(cliente.getVarianciaTempoEsperaFila2(EW2))
                somatorioVW2 += cliente.getVarianciaTempoEsperaFila2(EW2)
        EVW1 = somatorioVW1/len(self.__clientes)
        EVW2 = somatorioVW2/len(self.__clientes)

        EN1  = self.__somatorioPessoasFila1PorTempo       / (tempoAtual - self.__tempoInicial)
        ENq1 = self.__somatorioPessoasFilaEspera1PorTempo / (tempoAtual - self.__tempoInicial)
        EN2  = self.__somatorioPessoasFila2PorTempo       / (tempoAtual - self.__tempoInicial)
        ENq2 = self.__somatorioPessoasFilaEspera2PorTempo / (tempoAtual - self.__tempoInicial)

        # Impressao dos resultados das estatisticas
        #print "E[T1]:  %f" % (ET1)
        #print "E[W1]:  %f" % (EW1)
        #print "V(W1):  %f" % (EVW1)
        #print "E[N1]:  %f" % (EN1)
        #print "E[Nq1]: %f" % (ENq1)
        #print "E[T2]:  %f" % (ET2)
        #print "E[W2]:  %f" % (EW2)
        #print "V(W2):  %f" % (EVW2)
        #print "E[N2]:  %f" % (EN2)
        #print "E[Nq2]: %f" % (ENq2)

        #calculadora = CalculadoraIC()
        #print "IC E[T1]:  %f - %f" % (calculadora.intervaloDeConfiancaDeAmostras(clientesT1))
        #print "IC E[W1]:  %f - %f" % (calculadora.intervaloDeConfiancaDeAmostras(clientesW1))
        #print "IC V(W1):  %f - %f" % (calculadora.intervaloDeConfiancaDeAmostras(clientesVW1))
        #print "IC E[N1]:  %f - %f" % (calculadora.intervaloDeConfiancaDeAmostrasComMedia(self.__pessoasFila1PorTempo, EN1))
        #print "IC E[Nq1]: %f - %f" % (calculadora.intervaloDeConfiancaDeAmostrasComMedia(self.__pessoasFilaEspera1PorTempo, ENq1))
        #print "IC E[T2]:  %f - %f" % (calculadora.intervaloDeConfiancaDeAmostras(clientesT2))
        #print "IC E[W2]:  %f - %f" % (calculadora.intervaloDeConfiancaDeAmostras(clientesW2))
        #print "IC V(W2):  %f - %f" % (calculadora.intervaloDeConfiancaDeAmostras(clientesVW2))
        #print "IC E[N2]:  %f - %f" % (calculadora.intervaloDeConfiancaDeAmostrasComMedia(self.__pessoasFila2PorTempo, EN2))
        #print "IC E[Nq2]: %f - %f" % (calculadora.intervaloDeConfiancaDeAmostrasComMedia(self.__pessoasFilaEspera2PorTempo, ENq2))