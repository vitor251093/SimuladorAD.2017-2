from cliente import *

class Fila(object):

    def __init__(self, id):
        self.__id = id
        self.__clientes = []

    # Retorna cliente e remove do topo da array
    def retirarClienteEmAtendimento(self):
        pass

    # Entra com um cliente
    def adicionarClienteAFila(self, cliente):
        self.__clientes.append(cliente)

    # Retorna o cliente no indice zero (ponteiro)
    def clienteEmAtendimento(self):
        return Cliente[0]

    # Getters
    def getID(self):
        return self.__id

    # Setters
    def setID(self,id):
        self.__id = id