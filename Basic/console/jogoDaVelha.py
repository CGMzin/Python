#Jogo da Velha
campo = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9']]
numeros = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
win = 0
jogador = 0
letra = ''
print('''     _   _____   _____   _____        _____       ___        _     _   _____   _       _   _       ___  
    | | /  _  \ /  ___| /  _  \      |  _  \     /   |      | |   / / | ____| | |     | | | |     /   | 
    | | | | | | | |     | | | |      | | | |    / /| |      | |  / /  | |__   | |     | |_| |    / /| | 
 _  | | | | | | | |  _  | | | |      | | | |   / / | |      | | / /   |  __|  | |     |  _  |   / / | | 
| |_| | | |_| | | |_| | | |_| |      | |_| |  / /  | |      | |/ /    | |___  | |___  | | | |  / /  | | 
\_____/ \_____/ \_____/ \_____/      |_____/ /_/   |_|      |___/     |_____| |_____| |_| |_| /_/   |_| \n\n''')

def mostrarCampo():
    print("Campo atual:\n")
    for i in range (3):
        if i < 2:
            print(f"\033[4m {str(campo[i][0])} | {str(campo[i][1])} | {str(campo[i][2])}\033[0m")
        else:
            print(f" {str(campo[i][0])} | {str(campo[i][1])} | {str(campo[i][2])}\n")

def jogada(vez):
    if vez % 2 == 0:
        letra = "X"
    else:
        letra = "O"
    global campo
    print(f"Vez do jogador {letra}\n")
    correto = 0
    while correto == 0:
        casa = input("Em que casa você deseja jogar?\n")
        if casa in numeros:
            for i in range(3):
                for j in range(3):
                        if campo[i][j] == casa:
                            campo[i][j] = letra 
            correto = 1
        else:
            print("\nNão existe essa casa no campo, por favor, tente novamente!\n")
    return vez + 1

def verificar():
    global win
    if jogador == 9:
        win = 2
    for i in range(3):
        if campo[i][0] == campo[i][1] == campo[i][2]:
            win = 1
    for j in range(3):
        if campo[0][j] == campo[1][j] == campo[2][j]:
            win = 1
    if campo[0][0] == campo[1][1] == campo[2][2]:
        win = 1
    if campo[0][2] == campo[1][1] == campo[2][0]:
        win = 1    

while win == 0:
    if win == 0:
        mostrarCampo()
        jogador = jogada(jogador)
        print()
        verificar()
        if win != 0:
            mostrarCampo()
            if win == 1:
                if jogador % 2 == 0:
                    print("Vitória do jogador O!!!")
                else:
                    print("Vitória do jogador X!!!")
            else:
                print("Empate!")
            again = input("desejam jogar novamente (digite sim ou não)?\n")
            if again == "sim":  
                jogador = 0
                win = 0
                campo = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9']]