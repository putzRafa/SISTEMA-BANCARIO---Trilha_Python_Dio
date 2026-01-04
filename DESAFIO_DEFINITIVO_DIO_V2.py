from datetime import datetime
listUserCadastrados = []
listExtrato = []
contUser = 0

def log_transacao(funcao):
    def imprime_log(*args, **kwargs):
        match funcao.__name__: #verifica o nome da função
            case 'cria_usuario':
                agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                print(f"[{agora}] - Foi realizado o processo de Criaçao de usuário.\n")

            case 'deposito':
                agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                print(f"[{agora}] - Foi realizado o processo de Depósito.\n")

            case 'saque':
                agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                print(f"[{agora}] - Foi realizado o processo de Saque.\n")

            case 'imprime_extrato':
                agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                print(f"[{agora}] - Foi realizado o processo de Impressão de Extrato")

        return funcao(*args, **kwargs)

    return imprime_log

@log_transacao
def cria_usuario ():
    global contUser
    dictDeCadastro = dict.fromkeys(["nome", "data", "CPF", "saldo", "limite", "qtdSaque"])
    dictDeCadastro["limite"] = 500

    print("Insira seu nome de usuário:")
    nome = str(input())

    print("\nInsira sua data de nascimento:")
    while True:
        try:
            data = input()
            datetime.strptime(data, "%d/%m/%Y")
            break
        except ValueError:
            print("Formato inválido! Use dd/mm/aaaa.")

    print("\ninsira o CPF para cadastro:")
    cpf = str(input())

    while len(cpf) !=  11:
        print("CPF inválido. Insira corretamente. \n")
        cpf = str(input())

    dictDeCadastro["nome"] = nome
    dictDeCadastro["data"] = data
    dictDeCadastro["CPF"] = cpf
    dictDeCadastro["qtdSaque"] = 0

    if armazena_user(dictDeCadastro):
        cria_conta_corrente(dictDeCadastro, contUser)
        print("Usuário cadastrado com sucesso!")
        contUser += 1
    else:
        print("Cadastro Inválido")

    print(dictDeCadastro)
    armazena_extrato(cpf, 0, 0)
    return dictDeCadastro


def armazena_user(cadastro):
    for i in listUserCadastrados:
        if i["CPF"] == cadastro["CPF"]:
            print("CPF já cadastrado.")
            return False
        
    listUserCadastrados.append(cadastro)
    return True


def cria_conta_corrente(cadastro, numUsuario):
     cadastro["agencia"] = "0001"
     cadastro["digito"] = numUsuario
     cadastro["saldo"] = 0

@log_transacao
def deposito(valor, cpf, /):
    for usuario in listUserCadastrados:
        if usuario["CPF"] == cpf:
            usuario["saldo"] += valor
            print(f"Saldo atual: R$ {usuario['saldo']:.2f}")
            return 1
    return False

@log_transacao
def saque(*, valor, cpf):
    for usuario in listUserCadastrados:
        if usuario["CPF"] == cpf:

            if usuario["qtdSaque"] == 3:
                print("Limite de saques excedido. Não é possível mais realizar saques neste dia.")

            else:
                usuario["saldo"] -= valor
                print(f"Saldo atual: R$ {usuario['saldo']:.2f}")
                usuario["qtdSaque"] += 1
                return 2
    return False

def armazena_extrato(cpf, movimentacao, valor):
    for extrato in listExtrato:
        if extrato["CPF"] == cpf:
            if movimentacao == 1:
                extrato["movimentacao"].append({"tipo": "depósito", "valor": valor})

            if movimentacao == 2:
                extrato["movimentacao"].append({"tipo": "saque", "valor": valor})
            return 0

    nova_movimentacao = []

    if movimentacao == 1:
        nova_movimentacao.append({"tipo": "depósito", "valor": valor})

    elif movimentacao == 2:
        nova_movimentacao.append({"tipo": "saque", "valor": valor})

    elif movimentacao == 0:
        listExtrato.append({
        "CPF": cpf,
        "movimentacao": nova_movimentacao
        })
    return 0

@log_transacao
def imprime_extrato(cpf):

    for i in listExtrato:
        if i["CPF"] == cpf:
            print(f''' 
        ===========x=========
        Titular: {cpf}
''')
            
        if i["movimentacao"] == []:
            print("Não há movimentações nesta conta.\n\n")

        else:
            for mov in i["movimentacao"]:
                print(f" - tipo: {mov["tipo"]}  --- valor: R${mov["valor"]:.2f}")
    return 0

class ContaIterador():
    def __init__(self, lista: list[dict]):
        self.contador = 0
        self.lista = lista

    def __iter__(self):
        return self

    def __next__(self):
            if self.contador >= len(self.lista):
                raise StopIteration
            
            else:
                conta = self.lista[self.contador]
                self.contador += 1
                return conta
    
menu = """
[c] cria nova conta
[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair
[i] Imprimir Usuários

=> """

while True:
    opcao = input(menu)

    if opcao == "c":
        cria_usuario()

    elif opcao == "q":
        break

    elif opcao == "d":

        if listUserCadastrados == []:
            print("Não há usuários cadastrados no banco.")
        else:
            contaDeposito = str(input("Insira a conta para depósito (CPF): "))
            while len(contaDeposito) != 11:
                contaDeposito = str(input("CPF inválido. Insira a conta para saque (CPF): "))

            valor = float(input("Insira o valor do depósito: "))
            resultado = deposito(valor, contaDeposito)
            if resultado == 1:
                armazena_extrato(contaDeposito, resultado, valor)

    elif opcao == "s":
        if listUserCadastrados == []:
            print("Não ha usuários cadastrados no banco.")
        else:
            contaSaque = str(input("Insira a conta para saque (CPF): "))
            while len(contaSaque) != 11:
                contaSaque = str(input("CPF inválido. Insira a conta para saque (CPF): "))

            valor = float(input("Insira o valor do saque: "))
            while valor > 500:
                print("Valor de saque acima do limite. Limite acessível: R$ 500,00")
                valor = float(input("Insira o valor do saque: "))

            resultado = saque(valor = valor, cpf = contaSaque)
            if resultado == 2:
                armazena_extrato(contaSaque, resultado, valor)

    elif opcao == "e":
        if listExtrato == []:
            print("Não há contas cadastradas para exibir extrato.")

        else:   
            conta = str(input("Insira conta que deseja imprimir o extrato: "))
            while len(conta) != 11:
                print("CPF inválido. Tente novamente")
                conta = str(input("Insira conta que deseja imprimir o extrato: "))

            imprime_extrato(conta)

    elif opcao == "i":
        if listUserCadastrados == []:
            print("Sem usuários cadastrados.")
            
        else:
            contas = ContaIterador(listUserCadastrados)
            for i in contas:
                print(i)