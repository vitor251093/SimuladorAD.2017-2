from random import expovariate

class Agendador(object):

    def __init__(self):
        pass

    def agendarChegadaFila1(self, lambd):
        return expovariate(lambd)

    def agendarAtendimentoFila1(self, tempo_de_simulacao, tempo_de_servico):
        return tempo_de_simulacao + tempo_de_servico