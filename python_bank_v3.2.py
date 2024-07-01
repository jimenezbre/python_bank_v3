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

class Banco:
    def __init__(self):
        self.usuarios = {}
        self.contas = []
        self.numero_conta = 1000
        self.AGENCIA = "0001"

    def menu(self):
        print("Selecione uma opção:")
        print("1 - Sacar")
        print("2 - Depositar")
        print("3 - Extrato")
        print("4 - Criar conta")
        print("5 - Criar usuário")
        print("6 - Sair")
        return int(input())

    def selecionar_conta(self):
        numero_conta = int(input("Digite o número da conta: "))
        for conta in self.contas:
            if conta.numero == numero_conta:
                return conta
        print("Conta não encontrada.")
        return None

    def mostrar_extrato(self, conta):
        print("Seu extrato: ")
        for transacao in conta.historico.transacoes:
            if isinstance(transacao, Saque):
                print(f"Saque de: R$ {transacao.valor:.2f}")
            elif isinstance(transacao, Deposito):
                print(f"Depósito de: R$ {transacao.valor:.2f}")
        print(f"Saldo final: R$ {conta.saldo:.2f}")

    def criar_usuario(self):
        cpf = input("Qual o seu CPF? ")

        if cpf in self.usuarios:
            print("CPF já existente. Tente novamente!")
            return

        data_nasc = input("Qual a sua data de nascimento? ")
        nome = input("Qual o seu nome? ")
        endereco = input("Qual o seu endereço? ")

        self.usuarios[cpf] = PessoaFisica(cpf, nome, data_nasc, endereco)
        print("Usuário criado com sucesso!")

    def criar_conta(self):
        cpf = input("Qual o CPF do dono da conta? ")

        if cpf == '':
            return None
        if cpf not in self.usuarios:
            print("CPF inválido. Tente novamente! ou de Enter para retornar")
            return self.criar_conta()

        cliente = self.usuarios[cpf]
        conta = ContaCorrente(0.0, self.numero_conta, self.AGENCIA, cliente, limite=1000, limite_saques=3)
        cliente.adicionar_conta(conta)
        self.contas.append(conta)
        print(f"Agência: {self.AGENCIA}", f"Conta: {self.numero_conta} ", f"CPF: {cpf}")
        print("Conta criada com sucesso!")
        self.numero_conta += 1
        return conta

    def executar(self):
        while True:
            opcao = self.menu()

            if opcao == 1:
                valor = float(input("Qual o valor que deseja sacar? "))
                conta = self.selecionar_conta()
                if conta:
                    sucesso = conta.sacar(valor)
                    if sucesso:
                        print(f"Saque de R$ {valor:.2f} realizado com sucesso!")
                    else:
                        print("Saldo insuficiente ou limite de saque excedido.")
            elif opcao == 2:
                valor = float(input("Qual o valor que deseja depositar? "))
                conta = self.selecionar_conta()
                if conta:
                    conta.depositar(valor)
                    print(f"Depósito de R$ {valor:.2f} realizado com sucesso!")
            elif opcao == 3:
                conta = self.selecionar_conta()
                if conta:
                    self.mostrar_extrato(conta)
            elif opcao == 4:
                self.criar_conta()
            elif opcao == 5:
                self.criar_usuario()
            elif opcao == 6:
                print("Obrigado por utilizar o Python Bank!")
                break
            else:
                print("Opção inválida")

if __name__ == "__main__":
    banco = Banco()
    banco.executar()
