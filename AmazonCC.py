# Varíavel para saber se o usuário está logado
login = False

# Lista de compras temporária do carrinho
userTempPrice: []
userTempList: []


# Dados do Usuário
class usuarios:
    nome: None
    cpf: None
    senha: None
    email: None


# Produtos
class produtos:
    cod = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
    valor = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    nome = ['A arte da sedução por Andrei Braga', 'Arroz', 'Feijão', 'Carne',
            'Couro', 'Camisa', 'Tijolo', 'Kart', 'Carro', 'Moto', 'Meia', 'Bola',
            'Lápis', 'Caneta', 'Copo', 'Livro', 'Papel', 'Tesoura', 'Palito', 'Mesa']


# 1 - Cadastro
# Define uma função para cadastrar os novos clientes, se eles ja estiverem cadastrados ocorrerá um erro.
def cadastro(vetusuarios):
    '''
  :param vetusuarios: Banco de Dados com todos os usuários cadastrados
  :return: Retorna um novo usuário na variável vetusuarios
  '''
    usuario = usuarios()

    usuario.nome = input("Insira seu nome ")
    # Confere se o nome possui apenas letras
    nome = usuario.nome.isalpha()
    if nome == False:
        print('Nome incorreto!')
        continuar = input('\nDigite ENTER para continuar: ')
        return

    usuario.cpf = input("Insira seu cpf ")
    # Chama a função para validar CPF
    cpf = validarCPF(usuario.cpf)
    if cpf == False:
        print('CPF Incorreto')
        continuar = input('\nDigite ENTER para continuar: ')
        return
    # Testa se o CPF já está cadastrado
    for vetusario in vetusuarios:
        if usuario.cpf == vetusario.cpf:
            print("O CPF já existe")
            continuar = input('\nDigite ENTER para continuar: ')
            return

    usuario.senha = input("Insira sua senha ")
    # Verifica se a senha tem mais de 6 digitos
    if len(usuario.senha) < 6:
        print('Senha muito curta')
        continuar = input('\nDigite ENTER para continuar: ')
        return

    usuario.email = input("Insira seu email ")
    # Verifica se o email tem o caracter "@"
    if not '@' in usuario.email:
        print('Email inválido')
        continuar = input('\nDigite ENTER para continuar: ')
        return

    # Se tudo estiver de acordo, cadastra o usuário no nosso "Banco de Dados"
    vetusuarios.append(usuario)


# 2 - Consultar cliente
def consulta_cliente(cpf, vetusuarios):
    '''
    :param cpf: Recebe o CPF informado
    :param vetusuarios: Recebe todos os usuários cadastrados
    :return: Retorna o nome e email do cliente cadastrado
    '''
    for usuario in vetusuarios:
        if cpf == usuario.cpf:
            print(f"O nome do cliente é {usuario.nome}")
            print(f"O email do cliente é {usuario.email}")
        else:
            print('Usuário não cadastrado!')
    continuar = input('\nDigite ENTER para continuar: ')


# Lista produtos
def listar_produtos(vetprodutos):
    for prod in vetprodutos:
        print(prod.nome + " ", prod.valor)
    print()


# Compra
def comprar(vetusuarios):
    global login
    if login == False:
        p_email = input('Digite seu email: ')
        p_senha = input('Digite sua senha: ')
        for usuario in vetusuarios:
            if p_email == usuario.email and p_senha == usuario.senha:
                login = True
                print('Funcionou')
                break
            else:
                print('Login Incorreto!')
                continuar = input('\nDigite ENTER para continuar: ')
                return
    for pos in range(0, len(produtos.cod)):
        print(f'{produtos.cod[pos]:}', end='.')
        print(f'{produtos.nome[pos]:.<40}', end=' ')
        print(f'R$ {produtos.valor[pos]:.2f}', end='\n')
    global userTempPrice
    global userTempList
    userTempPrice = []
    userTempList = []
    item = -2
    while item != -1:
        print('Digite "-1" para parar')
        item = int(input('Digite o número do item que deseja comprar: '))
        if item < 0 and item >= 20:
            item = int(input('Digite um número válido do item que deseja comprar: '))
        if item >= 0 and item <= 19:
            userTempList.append(item)
            userTempPrice.append(produtos.valor[item])
    if sum(userTempPrice) <= 1000:
        continuar = input('\nCarrinho finalizado com sucesso! Digite ENTER para continuar: ')
    else:
        continuar = input('\nCrédito excedido! Digite ENTER para continuar: ')
        userTempPrice = []
        userTempList = []


# Mostrar carrinho
def ver_carrinho(vetusuarios):
    if login == False:
      print('Faça login primeiro!')
      continuar = input('\nDigite ENTER para continuar: ')
      return
    for c in userTempList:
        print(f'{c}', end='.')
        print(f'{produtos.nome[c]:.<40}', end=' ')
        print(f'R$ {produtos.valor[c]:.2f}')
    continuar = input('\nDigite ENTER para continuar: ')


# 5-Pagar conta
def pagar_conta(vetusuarios):
    if login == False:
      print('Faça login primeiro!')
      continuar = input('\nDigite ENTER para continuar: ')
      return
    ver_carrinho(vetusuarios)
    global userTempPrice
    global userTempList
    print(f'O total da sua conta é de R${sum(userTempPrice):.2f}')
    continuar = input('\nDigite ENTER para pagar: ')
    userTempList = []
    userTempPrice = []


def validarCPF(numbers):
    #  Obtém os números do CPF e ignora outros caracteres
    cpf = [int(char) for char in numbers if char.isdigit()]

    #  Verifica se o CPF tem 11 dígitos
    if len(cpf) != 11:
        return False

    #  Verifica se o CPF tem todos os números iguais, ex: 111.111.111-11
    #  Esses CPFs são considerados inválidos mas passam na validação dos dígitos
    #  Antigo código para referência: if all(cpf[i] == cpf[i+1] for i in range (0, len(cpf)-1))
    if cpf == cpf[::-1]:
        return False

    #  Valida os dois dígitos verificadores
    for i in range(9, 11):
        value = sum((cpf[num] * ((i + 1) - num) for num in range(0, i)))
        digit = ((value * 10) % 11) % 10
        if digit != cpf[i]:
            return False
    return True


# Menu Principal

def menu():
    opcao = "-1"
    vetusuarios = []
    vetprodutos = []
    while True:
        opcao = input(
            "Seja bem vindo! Esse é o menu principal, escolha dentre as seguinte opções:\n\n1- Cadastro\n2- Consultar cliente\n3- Comprar\n4- Carrinho de compras\n5- Pagar conta \n0- Sair\n")
        if opcao == "1":
            print("Opção selecionada: Cadastro")
            cadastro(vetusuarios)
        elif opcao == "2":
            print("Opção selecionada: Consultar cliente")
            parametro_consulta = input("Insira o CPF\n")
            consulta_cliente(parametro_consulta, vetusuarios)
        elif opcao == "3":
            print("Opção selecionada: Comprar")
            comprar(vetusuarios)
        elif opcao == "4":
            print("Opção selecionada: Carrinho de compras")
            ver_carrinho(vetusuarios)
        elif opcao == "5":
            print("Opção selecionada: Pagar conta")
            pagar_conta(vetusuarios)
        elif opcao == "6":
            print("Opção selecionada: Lista Produtos")
            listar_produtos(vetprodutos)
        elif opcao == "0":
            print("Opção selecionada: Sair")
            break
        else:
            print("Opção inválida, tente novamente")
menu()