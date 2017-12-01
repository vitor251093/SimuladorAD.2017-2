from random import expovariate

""" O Agendador sera responsavel por agendar chegadas e servicos
    de acordo com as taxas lambda e mi, respectivamente """

class Agendador(object):

    def __init__(self):
        pass

    def agendarChegadaFila1(self, lambd):
        return expovariate(lambd)

    def agendarTempoDeServicoFila1(self, mi):
        return expovariate(mi)

    def agendarTempoDeServicoFila2(self, mi):
        return expovariate(mi)