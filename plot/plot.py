import random
import numpy as numpy
import matplotlib.pyplot as pyplot
import sys

class Plot(object):

    def __init__(self):
        self.__colorSeed = 0
        self.__cores = []

    def numeroAleatorioDe0A255(self):
        self.__colorSeed += 60
        random.seed(self.__colorSeed)
        return int(round(random.random()*255))

    def corParaIndice(self, indice):
        if len(self.__cores) <= indice + 1:
            self.__cores.append("#%s%s%s" % (format(self.numeroAleatorioDe0A255(), '02X'),
                                             format(self.numeroAleatorioDe0A255(), '02X'),
                                             format(self.numeroAleatorioDe0A255(), '02X')))
        return self.__cores[indice + 1]

    def run(self):
        if len(sys.argv) <= 1:
            print "ERRO: O nome do arquivo .csv que sera plotado deve ser passado como argumento. Ele deve estar no mesmo diretorio do plot.py, ou entao o caminho do .csv inteiro devera ser passado."
            return

        N = numpy.loadtxt(sys.argv[1], unpack=True, delimiter=',')
        
        for indiceVetor in range(len(N[0])-1):
            valor1 = N[0][indiceVetor]
            valor2 = N[0][indiceVetor+1]
            cor    = int(N[1][indiceVetor])
            pyplot.plot([indiceVetor, indiceVetor+1], [valor1, valor2], self.corParaIndice(cor))

        #pyplot.title('')
        #pyplot.ylabel('')
        #pyplot.xlabel('')

        pyplot.show()


if __name__ == "__main__":
    Plot().run()
