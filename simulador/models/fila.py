from cliente import *

class Fila(object):

    def __init__(self, id):
        self.__id = id
        self.__clientes = []

    # Retorna cliente e remove do topo da array
    def retirarClienteEmAtendimento(self):
        cliente = self.__clientes[0]
        self.__clientes.pop(0)
        return cliente

    # Entra com um cliente
    def adicionarClienteAFila(self, cliente):
        self.__clientes.append(cliente)

    # Retorna o cliente no indice zero (ponteiro)
    def clienteEmAtendimento(self):
        return self.__clientes[0]

    # Numero de pessoas na fila
    def numeroDePessoasNaFila(self):
        return len(self.__clientes)

    # Getters
    def getID(self):
        return self.__id

    # Setters
    def setID(self,id):
        self.__id = id