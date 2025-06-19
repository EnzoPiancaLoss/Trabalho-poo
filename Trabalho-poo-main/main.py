
import cli
import data_base as banco_de_dado
import criar_banco_base as criar_bd_padrao
import utils
import classes as cla
main_menu = {
    "1": "Cadastrar itens",
    "2": "Exibir livros",
    "3": "Exibir usuarios",
    "4": "Realizar emprestimo",
    "5": "Devolver livro",
    "6": "Relatorios de disponibilidade",
    "7" : "Relatorios de emprestimos",
    "8" : "Atrasos"
}

# O parâmetro deve ser um dicionário
# Nunca pode conter a chave "0", pois ela está reservada para o botão de sair



def main():
    criar_padrao()
    while True:
        respota = cli.exibir_cli(main_menu)
        
        if respota == str(0):
            print("Tchau :)")
            break
        elif respota == str(1):
            Cadastrar_itens()
            pass
        elif respota == str(2):
            cli.mostrar_todos_os_itens("Livro")
            pass
        elif respota == str(3):
            cli.mostrar_todos_os_itens("Cliente")

        elif respota == str(4):
            resultado= cli.emprestimo()
            print(resultado)
            if resultado != None:
                banco_de_dado.Adicionar_dado_a_table_ESPECIFICO(
                    "Emprestimo",
                    ["id_livro","id_cliente","status","data_emprestimo","data_devolucao"],
                    [resultado["id_livro"], resultado["id_usuario"], resultado["status"], resultado["data_emprestimo"], resultado["data_devolucao"]]
                )

            pass
        elif respota == str(5):
            print(cli.devolver_livro())
            print("devolvido")
            pass
        elif respota == str(6):
            cli.relatorio_disponibilidade()
            pass
        elif respota == str(7):
            cli.relatorio_emprestimos()
            pass
        elif respota == str(8):
            cli.relatorio_atrasos()
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
        respota = cli.exibir_cli(Cadastro)

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
            elif respota == "3":
                banco_de_dado.cadastrar_autor()
                pass
            elif respota == "4":
                banco_de_dado.cadastrar_cliente()
                pass
            pass
        pass
    pass

    

def criar_padrao():
    criar_bd_padrao.criar_banco_padrao()
    utils.clean_terminal()
    pass

main()