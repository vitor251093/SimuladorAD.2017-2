from random import expovariate

class Agendador(object):

    def __init__(self):
        pass

    def agendarChegadaFila1(self, tempo_de_simulacao, lambd):
        return tempo_de_simulacao + expovariate(1.0/lambd)

    def agendarServicoFila1(self, tempo_de_simulacao, tempo_de_servico):
        return tempo_de_simulacao + tempo_de_servico