from abc import ABC, abstractmethod, abstractproperty

# classes abstrata
class Transacao(ABC):
    @abstractmethod
    def registrar(self):
        pass

class historico(Transacao):

    def registrar(self):
       print("Registro adicionado!")
    
    def adicionar_trasacao(self):
        print(f"Transacao adicionada {self.registrar()}")



extrato=historico().adicionar_trasacao()


class Cliente(self):
    pass


class Conta:

    def __init__(self,saldo,numero,agencia,cliente,historico):
        print("Teste")



