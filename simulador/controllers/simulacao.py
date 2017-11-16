class Simulacao(object):

    def __init__(self):
        self.__tempo = 0.0

    # Getters
    def getTempo(self):
        return self.__tempo

    # Setters
    def setTempo(self, tempo):
        self.__tempo = tempo