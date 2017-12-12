import random

""" O Agendador sera responsavel por agendar chegadas e servicos
    de acordo com as taxas lambda e mi, respectivamente."""

class Agendador(object):

    def __init__(self):
        self.__testeDeCorretude = False

    def setTesteDeCorretude(self, testeDeCorretude):
        self.__testeDeCorretude = testeDeCorretude

    def configurarSemente(self, seed):
        if self.__testeDeCorretude == True:
            return
        
        random.seed(seed)

    def agendarChegadaFila1(self, lambd):
        if self.__testeDeCorretude == True:
            return lambd

        return random.expovariate(lambd)

    def agendarTempoDeServicoFila1(self, mi):
        if self.__testeDeCorretude == True:
            return mi

        return random.expovariate(mi)

    def agendarTempoDeServicoFila2(self, mi):
        if self.__testeDeCorretude == True:
            return mi

        return random.expovariate(mi)