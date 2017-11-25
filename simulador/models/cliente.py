class Cliente(object):

    def __init__(self, id, tempoChegadaNoSistema):
        self.__id = id

        self.__tempoChegadaFila1 = tempoChegadaNoSistema
        self.__tempoChegadaServico1 = 0.0
        self.__tempoServico1 = 0.0

        self.__tempoChegadaFila2 = 0.0
        self.__tempoChegadaServico2 = 0.0
        self.__tempoServico2 = 0.0
        self.__tempoTerminoServico2 = 0.0
        self.__tempoNCServico2 = 0.0
        self.__tempoDecorridoServico2 = 0.0

    ## Setters
    def setID(self, id):
        self.__id = id

    def setTempoChegadaFila1(self, tempo):
        self.__tempoChegadaFila1 = tempo

    def setTempoChegadaServico1(self, tempo):
        self.__tempoChegadaServico1 = tempo

    def setTempoServico1(self, tempo):
        self.__tempoServico1 = tempo

    def setTempoChegadaFila2(self, tempo):
        self.__tempoChegadaFila2 = tempo

    def setTempoChegadaServico2(self, tempo):
        self.__tempoChegadaServico2 = tempo

    def setTempoServico2(self, tempo):
        self.__tempoServico2 = tempo

    def setTempoTerminoServico2(self, tempo):
        self.__tempoTerminoServico2 = tempo

    def setTempoNCServico2(self, tempo):
        self.__tempoNCServico2 = tempo

    def setTempoDecorridoServico2(self, tempo):
        self.__tempoDecorridoServico2 = tempo

    ## Getters
    def getID(self):
        return self.__id

    def getTempoChegadaFila1(self):
        return self.__tempoChegadaFila1

    def getTempoChegadaServico1(self):
        return self.__tempoChegadaServico1

    def getTempoTerminoServico1(self):
        return self.getTempoChegadaServico1() + self.getTempoServico1()

    def getTempoServico1(self):
        return self.__tempoServico1

    def getTempoChegadaFila2(self):
        return self.__tempoChegadaFila2

    def getTempoChegadaServico2(self):
        return self.__tempoChegadaServico2

    def getTempoServico2(self):
        return self.__tempoServico2

    def getTempoTerminoServico2(self):
        return self.__tempoTerminoServico2

    def getTempoNCServico2(self):
        return self.__tempoNCServico2

    def getTempoDecorridoServico2(self):
        return self.__tempoDecorridoServico2



    def getTempoEsperaFila1(self): # W1
        return self.getTempoChegadaServico1() - self.getTempoChegadaFila1()

    def getTempoTotalFila1(self): # T1
        return self.getTempoEsperaFila1() + self.getTempoServico1()

    def getVarianciaTempoEsperaFila1(self, esperancaTempoEsperaFila1): #VW1
        return (self.getTempoEsperaFila1() - esperancaTempoEsperaFila1) ** 2


    def getTempoEsperaFila2(self): # W2
        return self.getTempoChegadaServico2() - self.getTempoChegadaFila2()

    def getTempoTotalFila2(self): # T2
        return self.getTempoTerminoServico2() - self.getTempoChegadaFila2()

    def getVarianciaTempoEsperaFila2(self, esperancaTempoEsperaFila2): # VW2
        return (self.getTempoEsperaFila2() - esperancaTempoEsperaFila2) ** 2

    