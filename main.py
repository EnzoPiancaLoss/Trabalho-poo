from cli import exibir_cli
import data_base as banco_de_dado
import criar_banco_base as criar_bd_padrao
import utils
import classes as cla
main_menu = {
    "1": "Cadastrar itens",
    "2": "Exibir livros",
    "3": "Realizar emprestimo",
    "4": "Relatório de empréstimo"
}

# O parâmetro deve ser um dicionário
# Nunca pode conter a chave "0", pois ela está reservada para o botão de sair



def main():
    criar_padrao()
    while True:
        respota = exibir_cli(main_menu)
        
        if respota == str(0):
            print("Tchau :)")
            break
        elif respota == str(1):
            Cadastrar_itens()
            pass

        utils.clean_terminal()
        pass
    

def Cadastrar_itens():
    Cadastro = {
    "1": "Cadastrar Livros",
    "2": "Cadastrar Publicadora",
    "3": "Cadastrar Autor",
    "4": "Cadastrar Usuario"
    }

    while True:
        utils.clean_terminal()
        respota = exibir_cli(Cadastro)

        if respota == str(0):
            main()
            break
        elif int(respota) >= 1 and int(respota) <= 4:
            if respota == "1":
                #a = input()
                banco_de_dado.cadastrar_livro()
                pass
            elif respota == "2":
                banco_de_dado.cadastrar_Publicadora()
                pass
            pass
        pass
    pass

    

def criar_padrao():
    criar_bd_padrao.criar_banco_padrao()
    utils.clean_terminal()
    pass

main()