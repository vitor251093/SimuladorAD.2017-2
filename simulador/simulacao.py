from controllers.agendador import *
from models.cliente import *
from models.fila import *
from random import expovariate

class Simulacao(object):

    def __init__(self):
        self.__numero_de_clientes = 100
        self.__lambd = 1.0
        self.__tempo = 1000000.0
        self.__tempo_de_servico = 1.0

    def run(self):
        t = 0.0
        proxima_chegada = 0.0
        id_cliente = 0

        # A lista de Clientes fica no objeto Fila
        fila1 = Fila(1)

        # Agendador que controla as chegadas
        agendador = Agendador()

        while t < self.__tempo:
            if fila1.numeroDePessoasNaFila() == 0:
                proxima_chegada = agendador.agendarChegadaFila1(t, self.__lambd)
                inicio_de_servico = proxima_chegada
                print "Cliente 0 chega em: %f e inicia servico imediatamente." % (proxima_chegada)
            else:
                proxima_chegada = proxima_chegada + agendador.agendarChegadaFila1(t, self.__lambd)
                inicio_de_servico = max(proxima_chegada, fila1.getCliente(-1).getTempoTerminoServico1())

                if (proxima_chegada < fila1.getCliente(-1).getTempoTerminoServico1()):
                    print "Cliente %d chega na fila em: %f ." % (id_cliente, proxima_chegada)
                else:
                    print "Cliente %d estava sendo atendido enquanto Cliente %d chegou em %f" % (fila1.getCliente(-1).getID(), id_cliente, proxima_chegada)
                print "Cliente %d chega em: %f" % (id_cliente, proxima_chegada)

            cliente = Cliente(id_cliente, proxima_chegada, inicio_de_servico, self.__tempo_de_servico)
            fila1.adicionarClienteAFila(cliente)
            id_cliente+=1
            t = proxima_chegada


if __name__ == "__main__":
    Simulacao().run()
