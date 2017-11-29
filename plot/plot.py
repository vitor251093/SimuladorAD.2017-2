import numpy as numpy
import matplotlib.pyplot as pyplot

class Plot(object):

    def __init__(self):
        return

    def run(self):
        N = numpy.loadtxt('vetorEN10k.csv', unpack=True, delimiter=',')
        #N = [1,10,2,8,4,6,5,5,5,5]
        pyplot.plot(N)
        #pyplot.title('')
        #pyplot.ylabel('')
        #pyplot.xlabel('')

        pyplot.show()


if __name__ == "__main__":
    Plot().run()
