
from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime
import textwrap


class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf


class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0000"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero,cliente)
    
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
    
    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("\n@@@ Não é possível realizar a operação. Saldo insuficiente! @@@")

        elif valor > 0:
            self._saldo -= valor
            print("@@@ Saque realizado com sucesso! @@@")
            return True

        else:
            print("@@@ Não é possível realizar a operação. O valor informado é inválido! @@@")

        return False
    
    def depositar(self,valor):
        if valor > 0:
            self._saldo += valor
            print("@@@ Depósito realizado com sucesso! @@@")
        else:
            print("@@@ Não é possível realizar a operação. O valor informado é inválido! @@@")
            return False
        
        return True
                

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite = 500, limite_saques = 3) -> None:
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
            )
        
        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saques

        if excedeu_limite:
            print("@@@ Não é possível realizar a operação. O valor do saque excede o limite! @@@")

        elif excedeu_saques:
            print("@@@ Não é possível realizar a operação. Número máximo de saques excedido! @@@")

        else:
            return super().sacar(valor)
        
        return False
    
    def __str__(self) -> str:
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t{self.numero}
            Titular:\t{self.cliente.nome}
            """
    

class Historico:
    def __init__(self) -> None:
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
        )


class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass


class Saque(Transacao):
    def __init__(self, valor) -> None:
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    def __init__(self, valor) -> None:
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)
    

def menu():
    titulo = " MENU ".center(50,'=')
    menu = f"""\n
    {titulo}

    Escolha uma das opções abaixo para realizar uma
    operação bancária:
    
    [1]\tDepositar
    [2]\tSacar
    [3]\tExtrato
    [4]\tNova conta
    [5]\tListar contas
    [6]\tNovo usuário
    [7]\tSair
    => """
    return input(textwrap.dedent(menu))


def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None


def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\n@@@ Cliente não possui conta cadastrada! @@@")

    # FIXME: não permite cliente escolher a conta
    return cliente.contas[0]


def depositar(clientes):
    cpf = input("Insira o CPF do cliente:")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ O cliente não foi encontrado! @@@")
        return
    
    valor = float(input("Insira o valor a ser depositado:"))
    
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)

    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)


def sacar(clientes):
    cpf = input("Insira o CPF do cliente:")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ O cliente não foi encontrado! @@@")
        return

    valor = float(input("Insira o valor a ser sacado:"))
    
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)

    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)


def exibir_extrato(clientes):
    cpf = input("Insira o CPF do cliente:")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ O cliente não foi encontrado! @@@")
        return
    
    conta = recuperar_conta_cliente(cliente)

    if not conta:
        return
    
    print(" EXTRATO ".center(50,'='))
    transacoes = conta.historico.transacoes

    extrato = ""

    if not transacoes:
        extrato = "Nenhuma movimentação realizada."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR${transacao['valor']:.2f}"

    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("".center(50,'='))


def criar_cliente(clientes):
    cpf = input("Insira o CPF do cliente:")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("\n@@@ Já existe cliente com esse CPF! @@@")
        return
    
    nome = input("Insira o nome completo do cliente:")
    data_nascimento = input("Insira a data de nascimento (dd-mm-aaaa):")
    endereco = input("Insira o endereço (logradouro, número - bairro - cidade/sigla estado):")

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento,cpf=cpf,endereco=endereco)

    clientes.append(cliente)
    print("\n"," Cliente criado com sucesso!".center(50,'='))


def criar_conta(numero_conta, clientes, contas):
    cpf = input("Insira o CPF do cliente:")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ O cliente não foi encontrado. @@@")
        print("@@@ O fluxo de criação de conta será encerrado! @@@")
        return
    
    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)

    contas.append(conta)
    cliente.contas.append(conta)

    print("\n"," Conta criada com sucesso!".center(50,'='))

   
def listar_contas(contas):
    for conta in contas:
        print("=" * 50)
        print(textwrap.dedent(str(conta)))


def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "1":
            depositar(clientes)

        elif opcao == "2":
            sacar(clientes)

        elif opcao == "3":
            exibir_extrato(clientes)

        elif opcao == "4":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes,contas)

        elif opcao == "5":
            listar_contas(contas)

        elif opcao == "6":
            criar_cliente(clientes)

        elif opcao == "7":
            break

        else:
            print("\n@@@ Operação inválida, por favor selecione novamente a operação desejada. @@@")

main()

