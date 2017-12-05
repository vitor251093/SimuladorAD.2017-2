import random

class Agendador(object):

    def __init__(self):
        pass

    def configurarSemente(self, seed):
        random.seed(seed)

    def agendarChegadaFila1(self, lambd):
        return random.expovariate(lambd)

    def agendarTempoDeServicoFila1(self, mi):
        return random.expovariate(mi)

    def agendarTempoDeServicoFila2(self, mi):
        return random.expovariate(mi)