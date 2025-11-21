import json
import os
import random

ARQUIVO = "dados.json"

# ------------------ CARREGAR DADOS ------------------

def carregar_dados():
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, "r") as f:
            return json.load(f)
    return {"contas": {}}

# ------------------ SALVAR DADOS ------------------

def salvar_dados(dados):
    with open(ARQUIVO, "w") as f:
        json.dump(dados, f, indent=4)

# ------------------ RESETAR SISTEMA ------------------

def resetar_sistema():
    if os.path.exists(ARQUIVO):
        os.remove(ARQUIVO)
    print("\nSistema resetado com sucesso!\n")

# ------------------ CRIAR CONTA ------------------

def criar_conta(dados):
    print("\n--- CRIAR NOVA CONTA ---")
    usuario = input("Nome do usuário: ")

    numero_conta = str(random.randint(10_000_000_000, 99_999_999_999))
    saldo_inicial = random.randint(100, 500)  # Saldo aleatório
    limite = 500

    dados["contas"][numero_conta] = {
        "usuario": usuario,
        "saldo": saldo_inicial,
        "limite": limite,
        "extrato": []
    }

    salvar_dados(dados)

    print("\nConta criada com sucesso!")
    print(f"Usuário: {usuario}")
    print(f"Número da conta: {numero_conta}")
    print(f"Saldo inicial: R${saldo_inicial:.2f}\n")

# ------------------ LOGIN ------------------

def login(dados):
    print("\n--- LOGIN DE CONTA ---")
    numero = input("Digite o número da conta: ")

    if numero not in dados["contas"]:
        print("\nEssa conta não existe!")
        opc = input("Deseja criar uma nova conta? (S/N): ").upper()
        if opc == "S":
            criar_conta(dados)
        return None

    print("\nLogin realizado com sucesso!\n")
    return numero

# ------------------ MENU DA CONTA ------------------

def menu_conta(dados, conta):
    while True:
        info = dados["contas"][conta]

        print("\n-------------------------------------")
        print(f"Usuário: {info['usuario']}")
        print(f"Conta: {conta}")
        print(f"Saldo: R${info['saldo']:.2f}")
        print("-------------------------------------")

        print("[S] Sacar")
        print("[D] Depositar")
        print("[E] Extrato")
        print("[X] Sair da conta")
        print("-------------------------------------")

        opcao = input("=> ").upper()

        if opcao == "S":
            sacar(dados, conta)

        elif opcao == "D":
            depositar(dados, conta)

        elif opcao == "E":
            mostrar_extrato(dados, conta)

        elif opcao == "X":
            print("\nSaindo da conta...\n")
            break

        else:
            print("\nOpção inválida!\n")

# ------------------ FUNÇÕES BANCÁRIAS ------------------

def sacar(dados, conta):
    valor = float(input("\nValor para saque: R$ "))

    if valor <= 0:
        print("Valor inválido!")
        return

    if valor > dados["contas"][conta]["saldo"]:
        print("Saldo insuficiente!")
        return

    dados["contas"][conta]["saldo"] -= valor
    dados["contas"][conta]["extrato"].append(f"- R${valor:.2f}")
    salvar_dados(dados)

    print("Saque realizado com sucesso!")

def depositar(dados, conta):
    valor = float(input("\nValor para depósito: R$ "))

    if valor <= 0:
        print("Valor inválido!")
        return

    dados["contas"][conta]["saldo"] += valor
    dados["contas"][conta]["extrato"].append(f"+ R${valor:.2f}")
    salvar_dados(dados)

    print("Depósito realizado com sucesso!")

def mostrar_extrato(dados, conta):
    print("\n------ EXTRATO ------")

    extrato = dados["contas"][conta]["extrato"]

    if len(extrato) == 0:
        print("Nenhuma movimentação.")
    else:
        for mov in extrato:
            print(mov)

    print(f"\nSaldo atual: R${dados['contas'][conta]['saldo']:.2f}")
    print("----------------------\n")


# ------------------ MENU PRINCIPAL ------------------

def main():
    dados = carregar_dados()

    while True:
        print("========== SISTEMA BANCÁRIO ==========")
        print("[C] Criar conta")
        print("[L] Login em conta existente")
        print("[R] Resetar sistema")
        print("[X] Sair")
        print("======================================")

        opc = input("=> ").upper()

        if opc == "C":
            criar_conta(dados)

        elif opc == "L":
            conta = login(dados)
            if conta:
                menu_conta(dados, conta)

        elif opc == "R":
            resetar_sistema()
            dados = carregar_dados()

        elif opc == "X":
            print("\nEncerrando o sistema...")
            break

        else:
            print("\nOpção inválida!\n")


main()