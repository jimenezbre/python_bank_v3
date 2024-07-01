

def main():

    AGENCIA = "0001"
    saldo = 0
    extrato = [f"\nSeu saldo inicial é de: R$ {saldo:.2f}\n"]
    limite_saque = 500
    limite_saque_restante = 3
    numero_conta = 0
    contas = []
    usuarios = []
    while True:
        opcao = menu()
    
        if opcao == 1:
            valor = float(input("Qual o valor que deseja sacar? "))
            sacar(saldo=saldo, valor=valor, extrato=extrato, limite_saque=limite_saque, limite_saque_restante=limite_saque_restante)
        elif opcao == 2:
            valor = float(input("Qual o valor que deseja depositar? "))
            depositar(saldo, valor, extrato)
        elif opcao == 3:
            mostrar_extrato(saldo, extrato=extrato)
        elif opcao == 4:
            numero_conta += 1
            conta = criar_conta(agencia=AGENCIA, numero_conta=numero_conta, usuarios=usuarios)
            if conta is None:
                print("Tente novamente!")
                return
            contas.append(conta)
        elif opcao == 5:
            criar_usuario(usuarios=usuarios)
        elif opcao == 6:
            print("Obrigado por utilizar o Python Bank!")
            quit()
        else :
            print("Opcão inválida")

def criar_usuario(usuarios):
    cpf = input("Qual o seu CPF? ")

    if cpf in usuarios:
        print("CPF já existente. Tente novamente!")
        return criar_usuario(usuarios)

    data_nasc = input("Qual a sua data de nascimento? ")
    nome = input("Qual o seu nome? ")
    endereco = input("Qual o seu endereço? ")

    usuarios.append({'nome':nome, 'cpf':cpf, 'data_nasc':data_nasc, 'endereco':endereco})
    print("Conta criada com sucesso!")

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Qual o CPF do dono da conta? ")

    if cpf == '':
        return
    if cpf not in usuarios:
        print("CPF inválido. Tente novamente! ou de Enter para retornar")
        return criar_conta(agencia, numero_conta, usuarios)
    print("Conta criada com sucesso!")
    return {'agencia':agencia, 'numero_conta':numero_conta, 'cpf':cpf}

def menu():
    print("Selecione uma opção:")
    print("1 - Sacar")
    print("2 - Depositar")
    print("3 - Extrato")
    print("4 - Criar conta")
    print("5 - Criar usuário")
    print("6 - Sair")
    return int(input())

def sacar(*, saldo, valor, extrato, limite_saque, limite_saque_restante):

    if limite_saque_restante <= 0:
        print("Você atingiu o limite de saques diários.")
        return
    if valor > limite_saque:
        print("Limite de saque excedido")
    elif valor > saldo:
        print("Saldo insuficiente")
    elif valor <= 0:
        print("Valor inválido")
    else:
        saldo -= valor
        limite_saque_restante -= 1
        extrato.append(f"\nSaque de: R$ {valor:.2f}\n")
        print(f"Seu novo saldo é de: R$ {saldo:.2f}")
        
def depositar(saldo, valor, extrato, /):
    if valor <= 0:
        print("Valor inválido")
    else:
        saldo += valor
        extrato.append(f"\nDeposito de: R$ {valor:.2f}\n Seu novo saldo é de: R$ {saldo:.2f}\n")
        print(f"Seu novo saldo é de: R$ {saldo:.2f}")

def mostrar_extrato(saldo, /, *, extrato):
    print("Seu extrato: ")
    for i in extrato:
        print(i)
    print(f"Seu saldo final é de: R$ {saldo:.2f}")

main()
