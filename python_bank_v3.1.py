from abc import ABC, abstractmethod
from datetime import date

class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append(transacao)

class Transacao(ABC):
    @abstractmethod
    def registrar(self, conta):
        pass

class Deposito(Transacao):
    def __init__(self, valor: float):
        self.valor = valor

    def registrar(self, conta):
        conta.saldo += self.valor
        conta.historico.adicionar_transacao(self)

class Saque(Transacao):
    def __init__(self, valor: float):
        self.valor = valor

    def registrar(self, conta):
        if conta.saldo >= self.valor:
            conta.saldo -= self.valor
            conta.historico.adicionar_transacao(self)
            return True
        return False

class Conta:
    def __init__(self, saldo: float, numero: int, agencia: str, cliente):
        self.saldo = saldo
        self.numero = numero
        self.agencia = agencia
        self.cliente = cliente
        self.historico = Historico()

    def saldo(self):
        return self.saldo

    def nova_conta(cliente, numero: int):
        return Conta(0.0, numero, "0000", cliente)

    def sacar(self, valor: float) -> bool:
        transacao = Saque(valor)
        return transacao.registrar(self)

    def depositar(self, valor: float) -> bool:
        transacao = Deposito(valor)
        transacao.registrar(self)
        return True

class Cliente:
    def __init__(self, endereco: str):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta: Conta, transacao: Transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta: Conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, cpf: str, nome: str, data_nascimento: date, endereco: str):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento

class ContaCorrente(Conta):
    def __init__(self, saldo: float, numero: int, agencia: str, cliente, limite: float, limite_saques: int):
        super().__init__(saldo, numero, agencia, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

def main():
    usuarios = {}
    contas = []
    numero_conta = 1000
    AGENCIA = "0001"

    while True:
        opcao = menu()
    
        if opcao == 1:
            valor = float(input("Qual o valor que deseja sacar? "))
            conta = selecionar_conta(contas)
            if conta:
                sucesso = conta.sacar(valor)
                if sucesso:
                    print(f"Saque de R$ {valor:.2f} realizado com sucesso!")
                else:
                    print("Saldo insuficiente ou limite de saque excedido.")
        elif opcao == 2:
            valor = float(input("Qual o valor que deseja depositar? "))
            conta = selecionar_conta(contas)
            if conta:
                conta.depositar(valor)
                print(f"Depósito de R$ {valor:.2f} realizado com sucesso!")
        elif opcao == 3:
            conta = selecionar_conta(contas)
            if conta:
                mostrar_extrato(conta)

        elif opcao == 4:
            numero_conta += 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)
            if conta:
                contas.append(conta)
        elif opcao == 5:
            criar_usuario(usuarios)
        elif opcao == 6:
            print("Obrigado por utilizar o Python Bank!")
            break
        else:
            print("Opção inválida")



def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Qual o CPF do dono da conta? ")

    if cpf == '':
        return None
    if cpf not in usuarios:
        print("CPF inválido. Tente novamente! ou de Enter para retornar")
        return criar_conta(agencia, numero_conta, usuarios)

    cliente = usuarios[cpf]
    conta = ContaCorrente(0.0, numero_conta, agencia, cliente, limite=1000, limite_saques=3)
    cliente.adicionar_conta(conta)
    print(f"Agência: {agencia}", f"Conta: {numero_conta} ", f"CPF: {cpf}")
    print("Conta criada com sucesso!")
    return conta

def menu():
    print("Selecione uma opção:")
    print("1 - Sacar")
    print("2 - Depositar")
    print("3 - Extrato")
    print("4 - Criar conta")
    print("5 - Criar usuário")
    print("6 - Sair")
    return int(input())

def selecionar_conta(contas):
    numero_conta = int(input("Digite o número da conta: "))
    for conta in contas:
        if conta.numero == numero_conta:
            return conta
    print("Conta não encontrada.")
    return None

def mostrar_extrato(conta):
    print("Seu extrato: ")
    for transacao in conta.historico.transacoes:
        if isinstance(transacao, Saque):
            print(f"Saque de: R$ {transacao.valor:.2f}")
        elif isinstance(transacao, Deposito):
            print(f"Depósito de: R$ {transacao.valor:.2f}")
    print(f"Saldo final: R$ {conta.saldo:.2f}")
def criar_usuario(usuarios):
    cpf = input("Qual o seu CPF? ")

    if cpf in usuarios:
        print("CPF já existente. Tente novamente!")
        return

    data_nasc = input("Qual a sua data de nascimento? ")
    nome = input("Qual o seu nome? ")
    endereco = input("Qual o seu endereço? ")

    usuarios[cpf] = PessoaFisica(cpf, nome, data_nasc, endereco)
    print("Usuário criado com sucesso!")

main()
