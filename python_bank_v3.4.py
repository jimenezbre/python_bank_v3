from abc import ABC, abstractmethod
from datetime import date

class Historico:
    def __init__(self):
        self._transacoes = []
        self._saques_realizados = 0

    def adicionar_transacao(self, transacao):
        self._transacoes.append(transacao)

    @property
    def transacoes(self):
        return self._transacoes
    
    @property
    def saques_realizados(self):
        return self._saques_realizados

class Transacao(ABC):
    @abstractmethod
    def registrar(self, conta):
        pass

class Deposito(Transacao):
    def __init__(self, valor: float):
        self._valor = valor

    def registrar(self, conta):
        conta._saldo += self._valor
        conta.historico.adicionar_transacao(self)

    @property
    def valor(self):
        return self._valor

class Saque(Transacao):
    def __init__(self, valor: float):
        self._valor = valor

    def registrar(self, conta):
            if (conta._saldo >= self._valor and
                self._valor <= conta._limite and
                conta._historico.saques_realizados < conta._limite_saques):
                
                conta._saldo -= self._valor
                conta._historico.adicionar_transacao(self)
                conta._historico._saques_realizados += 1
                return True
            return False

    @property
    def valor(self):
        return self._valor

class Conta:
    def __init__(self, saldo: float, numero: int, agencia: str, cliente):
        self._saldo = saldo
        self._numero = numero
        self._agencia = agencia
        self._cliente = cliente
        self._historico = Historico()


    @staticmethod
    def nova_conta(cliente, numero: int):
        return Conta(0.0, numero, "0000", cliente)

    def sacar(self, valor: float) -> bool:
        transacao = Saque(valor)
        return transacao.registrar(self)

    def depositar(self, valor: float) -> bool:
        transacao = Deposito(valor)
        transacao.registrar(self)
        return True

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

class Cliente:
    def __init__(self, endereco: str):
        self._endereco = endereco
        self._contas = []

    def realizar_transacao(self, conta: Conta, transacao: Transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta: Conta):
        self._contas.append(conta)

    @property
    def endereco(self):
        return self._endereco

    @property
    def contas(self):
        return self._contas

class PessoaFisica(Cliente):
    def __init__(self, cpf: str, nome: str, data_nascimento: date, endereco: str):
        super().__init__(endereco)
        self._cpf = cpf
        self._nome = nome
        self._data_nascimento = data_nascimento

    @property
    def cpf(self):
        return self._cpf

    @property
    def nome(self):
        return self._nome

    @property
    def data_nascimento(self):
        return self._data_nascimento

class ContaCorrente(Conta):
    def __init__(self, saldo: float, numero: int, agencia: str, cliente, limite: float, limite_saques: int):
        super().__init__(saldo, numero, agencia, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    @property
    def limite(self):
        return self._limite

    @property
    def limite_saques(self):
        return self._limite_saques

class Banco:
    def __init__(self):
        self._usuarios = {}
        self._contas = []
        self._numero_conta = 1000
        self._AGENCIA = "0001"

    def menu(self):
        print("Selecione uma opção:")
        print("1 - Sacar")
        print("2 - Depositar")
        print("3 - Extrato")
        print("4 - Criar conta")
        print("5 - Criar usuário")
        print("6 - Sair")
        return input()

    def selecionar_conta(self):
        numero_conta = int(input("Digite o número da conta: "))
        for conta in self._contas:
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

        if cpf in self._usuarios:
            print("CPF já existente. Tente novamente!")
            return

        data_nasc = input("Qual a sua data de nascimento? ")
        nome = input("Qual o seu nome? ")
        endereco = input("Qual o seu endereço? ")

        self._usuarios[cpf] = PessoaFisica(cpf, nome, data_nasc, endereco)
        print("Usuário criado com sucesso!")

    def criar_conta(self):
        cpf = input("Qual o CPF do dono da conta? ")

        if cpf == '':
            return None
        if cpf not in self._usuarios:
            print("CPF inválido. Tente novamente! ou de Enter para retornar")
            return self.criar_conta()

        cliente = self._usuarios[cpf]
        conta = ContaCorrente(0.0, self._numero_conta, self._AGENCIA, cliente, limite=500, limite_saques=3)
        cliente.adicionar_conta(conta)
        self._contas.append(conta)
        print(f"Agência: {self._AGENCIA}", f"Conta: {self._numero_conta} ", f"CPF: {cpf}")
        print("Conta criada com sucesso!")
        self._numero_conta += 1
        return conta

    def executar(self):
        while True:
            opcao = self.menu()
            try:
                opcao = int(opcao)
            except ValueError:
                print("Opção inválida. Deve ser um número inteiro.")
                continue

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
