from random import expovariate

class Agendador(object):

    def __init__(self):
        pass

    def agendarChegadaFila1(self, lambd):
        return expovariate(lambd)

    def agendarTempoDeServicoFila1(self, tempo_de_servico):
        return tempo_de_servico

    def agendarTempoDeServicoFila2(self, tempo_de_servico):
        return tempo_de_servico