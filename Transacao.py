from abc import ABC, abstractmethod, abstractproperty

## INICIO DEFINIÇÃO DE CLASSES
# classes abstrata
class Transacao(ABC):
    @abstractmethod
    def registrar(self,conta):
        pass
    # não tem no modelo, mas faz sentido haver um valor
    @abstractproperty
    def valor(self):
        pass

class Deposito(Transacao):
    def __init__(self,valor):
        self._valor=valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso=conta.depositar(self.valor)

        if sucesso:
            conta.historico.adicionarTransacao(self)
        
    
class Saque(Transacao)    :
    def __init__(self,valor):
        self._valor=valor
    @property
    def valor(self)    :
        return self._valor
    
    def registrar(self,conta):
        sucesso=conta.sacar(self.valor)
        if sucesso:
            conta.historico.adicionarTransacao(self)
    
class Historico:
    def __init__(self):
        self._transacoes=[] # minha lista de transacoes

    @property
    def transacoes(self):
        return  self._transacoes
    
    def adicionarTransacao(self,transacao):
        self._transacoes.append("Uma transação foi adicionada ao histórico")
        self._transacoes.append({"tipo":transacao.__class__.__name__,"valor":transacao.valor})
            
class Cliente:
    def __init__(self,endereco):
        self.endereco=endereco
        self.contas=[]
    
    def realizarTransacoes(self,conta,transacao):
       transacao.registrar(conta)

    def adicionarConta(self,conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self,cpf,nome,dataNascimento,endereco):
        super().__init__(endereco)
        self.cpf=cpf
        self.nome=nome
        self.dataNascimento=dataNascimento

class Conta:
    def __init__(self,numero,cliente):
        self._saldo=0
        self._numero=numero
        self._agencia="0001"
        self._cliente=cliente
        self._historico=Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)    

    @property
    def saldo(self):
        return self._saldo
    @property
    def numero(self):
        return self._numero
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico
    
    def sacar(self,valor):
        

        if valor> self.saldo:
            print("Operação encerrada por falta de saldo")
        elif valor>0:
            self._saldo-=valor    
            print("Saque realizado com sucesso")
            return True
        else:
            print("Operação falhou,valor inválido!")
            return False
    def depositar(self, valor):
        if valor >0 :
            self._saldo+=valor
            print("Valor depositado com sucesso!")
        else:
            print("Operação falhou, pois o valor é inválido!")

class ContaCorrente(Conta):
    def __init__(self,numero,cliente,limite=500,limiteSaques=3):
        super().__init__(numero,cliente)
        self._limite=limite
        self._limiteSaques=limiteSaques
    
    def sacar(self,valor):
        qtSaques= len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"]==Saque.__name__]
        )
        excedeu_limite=valor>self._limite
        excedeu_saques=qtSaques > self._limiteSaques

        if excedeu_limite:
            print("O valor está acima do seu limite de saque")
        elif excedeu_saques:
            print("Você ultrapassou seu limite de saques!")
        else:
            return super().sacar(valor)   
        return False
    
    # Função copiada do exemplo
    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """


## FIM DA DEFINIÇÃO DE CLASSES
    

## INICIO DEFINIÇÃO DE FUNÇÕES
    # parametros precisam ser passados diretos.Ex:deposito(100,10,"")

def deposito(clientes):
    cpf=input("Informe o CPF do cliente")
    cliente=buscaUsuario(cpf,clientes)
    
    if not cliente:
        print("O cliente não foi encontrado!")
        return
    valor=float(input("Informe o valor para deposito: "))
    transacao=Deposito(valor)
    conta=recuperarContaCliente(cliente)
    if not conta:
        return
    cliente.realizarTransacoes(conta,transacao)

# exemplo saque(*,saldo=saldo,valor=valor):
def recuperarContaCliente(cliente):
    if not cliente.contas:
        print("Cliente não possui conta")
        return
    return cliente.contas[0] # esta implementação não permite o cliente ter mais do que uma conta


def saque(clientes):
    cpf=input("Informe o CPF do cliente")
    cliente=buscaUsuario(cpf,clientes)
    
    if not cliente:
        print("O cliente não foi encontrado!")
        return
    valor=float(input("Informe o valor para saque: "))
    transacao=Saque(valor)
    conta=recuperarContaCliente(cliente)
    if not conta:
        return
    cliente.realizarTransacoes(conta,transacao)

    
    

def extrato(clientes):    
    cpf=input("Informe o CPF do cliente")
    cliente=buscaUsuario(cpf,clientes)
    
    if not cliente:
        print("O cliente não foi encontrado!")
        return
    conta=recuperarContaCliente(cliente)

    if not conta:
        print("Cliente sem conta!")
        return
    print("*****EXTRATO*****")
    transacoes=conta.historico.transacoes
    extrato=""
    if not transacoes:
        print("Não há registro de transações")
    else:
        for t in transacoes:
            #extrato+=f"\n{t['tipo']}:\n\tR${t['valor']:.2f}"
            print(t)
        
        print(extrato)
        print(f"\nSaldo:\n\tR${conta.saldo:.2f}")
        print("*****************")


    
    
    


def criaUsuario(clientes):
    cpf=input("Digite o CPF (SOMENTE NÚMEROS): ")
    cliente=buscaUsuario(cpf,clientes)

    if cliente:
        print("Usuário já cadastrado!")
        return

    nome=input("Informe seu nome: ")
    data_nascimento=input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco=input("Informe o endereço (logradouro,nro-bairro-cidade/sigla estado): ")
    
    cliente=PessoaFisica(cpf=cpf,nome=nome,dataNascimento=data_nascimento,endereco=endereco)
    clientes.append(cliente)
   
    print("Cliente cadastrado com sucesso")

def buscaUsuario(cpf,clientes):
    clienteFiltrado=[cliente for cliente in clientes if cliente.cpf==cpf]    
    return clienteFiltrado[0] if clienteFiltrado else None

def criarConta(num_conta,clientes,contas):
    cpf=input("Informe o CPF: ")
    cliente=buscaUsuario(cpf,clientes)

    if not cliente:
        print("Cliente não encontrado")
        return
    conta=ContaCorrente.nova_conta(cliente=cliente,numero=num_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print("Conta criada com sucesso!")

def listaClientes(clientes):
    for c in clientes:
        print("*"*100)
        print(f"Nome :{c.nome}")
        print(f"CPF :{c.cpf}")        
        print(f"Endereco :{c.endereco}")
        

def listaContas(contas):
   for conta in contas:
       print("*"*10)
       print(str(conta))

## FIM DEFINIÇÃO DAS FUNÇÕES        


def menu():
    menu = "************************************\n"
    menu += "*[1]-Extrato                       *\n"
    menu += "*[2]-Depósito                      *\n"
    menu += "*[3]-Saque                         *\n"
    menu += "*[4]-Novo cliente                  *\n"
    menu += "*[5]-Nova conta                    *\n"
    menu += "*[6]-Listagem cliente              *\n"
    menu += "*[7]-Listagem conta                *\n"
    menu += "*[8]-Sair do programa              *\n"
    menu += "************************************\n"

    return int(input(menu))


def main():    
    opcao=0   
    clientes=[]    
    contas=[]
    while opcao!=8:
        try:
            opcao=menu()       
        except ValueError:
            print("Escolha inválida!")    
        
        if opcao==1:
            extrato(clientes)    
         #deposito   
        elif opcao==2:
            deposito(clientes)
        #saque
        elif opcao==3:
            saque(clientes)

        # lista de clientes
        if opcao==4:           
           criaUsuario(clientes)
        
        if opcao==5:            
            num_conta=len(contas)+1
            criarConta(num_conta,clientes,contas)            

        if opcao==6:
            listaClientes(clientes)
            

        if opcao==7:
            listaContas(contas)      

main()