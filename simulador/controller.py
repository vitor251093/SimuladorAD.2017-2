from models.cliente import *
from random import expovariate

# Essa funcao eh soh um exemplo de como fazer para agendar as chegadas
def rodar():
    numero_clientes = 20
    lista_de_clientes = []
    lambd = 0.1
    tempo_simulacao = 0.0

    for i in xrange(numero_clientes):
        # Agenda proxima chegada
        # o intervalo da proxima chegada eh definido por expovariate
        proxima_chegada = tempo_simulacao + expovariate(0.1)

        # Cria cliente e adiciona num vetor de clientes
        c = Cliente()
        c.setID(i)
        c.setTempoChegadaFila1(proxima_chegada)
        lista_de_clientes.append(c)

        # Imprime pra ver como esta
        print "Cliente %d chegou no instante: %f" % (c.getID(), c.getTempoChegadaFila1())

        # Seta tempo de simulacao como tempo da chegada (a proxima chegada deve ocorrer apos)
        tempo_simulacao = proxima_chegada




if __name__ == "__main__":
    rodar()