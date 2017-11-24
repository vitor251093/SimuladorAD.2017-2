from random import expovariate

class Agendador(object):

    def __init__(self):
        pass

    def agendarChegadaFila1(self, lambd):
        return expovariate(lambd)

    def agendarTempoDeServicoFila1(self, mi):
        return 2.0

    def agendarTempoDeServicoFila2(self, mi):
        return 3.0