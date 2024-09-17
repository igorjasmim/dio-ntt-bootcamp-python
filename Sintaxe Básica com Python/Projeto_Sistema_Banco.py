# Criando um menu de interface com o usuário:
menu = """

Escolha uma das opções abaixo para realizar uma operação bancária:
[1] Depositar
[2] Sacar
[3] Extrato
[4] Sair

=> """

saldo = 0           # iniciando o saldo
limite = 500        # limite de saque
extrato = ""        # iniciando o extrato
numero_saques = 0   # iniciando o número de saques
LIMITE_SAQUES = 3   # limite de operações de saque

while True:

    opcao = input(menu)

    # Opção Depositar:
    if opcao == "1":
        valor = float(input("Informe o valor do depósito: "))

        if valor > 0:
            saldo += valor
            extrato += f"Depósito: R$ {valor:.2f}\n"

        else:
            print("Operação falhou! O valor informado é inválido.")
    # Opção Sacar:
    elif opcao == "2":
        valor = float(input("Informe o valor do saque: "))

        if valor > saldo:
            print("Operação falhou! Você não tem saldo suficiente.")

        elif valor > limite:
            print("Operação falhou! O valor do saque excede o limite.")

        elif numero_saques >= LIMITE_SAQUES:
            print("Operação falhou! Número máximo de saques excedido.")

        elif valor > 0:
            saldo -= valor
            extrato += f"Saque: R$ {valor:.2f}\n"
            numero_saques += 1

        else:
            print("Operação falhou! O valor informado é inválido.")

    # Opção Extrato:
    elif opcao == "3":
        print(" EXTRATO ".center(50,'#'))
        print("Não foram realizadas movimentações." if not extrato else extrato)
        print(f"\nSaldo: R$ {saldo:.2f}".ljust(50))
        print(" FIM EXTRATO ".center(50,'#'))

    # Opção Sair:
    elif opcao == "4":
        break
    
    # Opção caso digite algo diferente das operações:
    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")
