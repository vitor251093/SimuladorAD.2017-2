# ID
#
# Tempo de chegada na fila 1
# Tempo de chegada no serviço 1
# Tempo de têrmino do serviço 1
# Tempo de serviço 1
#
# Tempo de chegada na fila 2
# Tempo de chegada no serviço 2
# Tempo de têrmino do serviço 2
# Tempo não-contínuo de serviço 2
# Tempo decorrido de serviço 2
class Cliente(object):

    def __init__(self):
        self.__tempoChegadaFila1 = 0.0
        self.__tempoChegadaServico1 = 0.0
        self.__tempoTerminoServico1 = 0.0
        self.__tempoServico1 = 0.0

        self.__tempoChegadaFila2 = 0.0
        self.__tempoChegadaServico2 = 0.0
        self.__tempoTerminoServico2 = 0.0
        self.__tempoNCServico2 = 0.0
        self.__tempoDecorridoServico2 = 0.0

    ## Setters
    def setTempoChegadaFila1(self, tempo):
        self.__tempoChegadaFila1 = tempo

    def setTempoChegadaServico1(self, tempo):
        self.__tempoChegadaServico1 = tempo

    def setTempoTerminoServico1(self, tempo):
        self.__tempoTerminoServico1 = tempo

    def setTempoServico1(self, tempo):
        self.__tempoServico1 = tempo

    def setTempoChegadaFila2(self, tempo):
        self.__tempoChegadaFila2 = tempo

    def setTempoChegadaServico2(self, tempo):
        self.__tempoChegadaServico2 = tempo

    def setTempoTerminoServico2(self, tempo):
        self.__tempoTerminoServico2 = tempo

    def setTempoNCSerivico2(self, tempo):
        self.__tempoNCServico2 = tempo

    def setTempoDecorridoServico2(self, tempo):
        self.__tempoDecorridoServico2 = tempo

    ## Getter
    def getTempoChegadaFila1(self, tempo):
        self.__tempoChegadaFila1 = tempo

    def getTempoChegadaServico1(self, tempo):
        self.__tempoChegadaServico1 = tempo

    def getTempoTerminoServico1(self, tempo):
        self.__tempoTerminoServico1 = tempo
