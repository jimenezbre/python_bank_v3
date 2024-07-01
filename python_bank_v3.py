from abc import ABC, abstractmethod
from datetime import date
from typing import List

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

    def saldo(self) -> float:
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
