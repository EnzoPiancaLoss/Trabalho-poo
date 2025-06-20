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
    "8" : "Atrasos",
    "9" : "Editar itens",
    "10" : "Excluir dados"
}

# O parâmetro deve ser um dicionário
# Nunca pode conter a chave "0", pois ela está reservada para o botão de sair



def main():
    utils.clean_terminal()
    criar_padrao()
    while True:
        respota = cli.exibir_cli(main_menu, "Sair")
        
        if respota == str(0):
            utils.terminate()
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
        elif respota == str(9):
            Cadastrar_itens(True)
        elif respota == str(10):
            excluir()
        utils.clean_terminal()
        pass
    

def tratar_cadastro_ou_edicao(tipo, edicao):
    """
    tipo: str ("1", "2", "3", "4")
    edicao: bool
    """
    try:
        if edicao:
            inputt = input(f"Insira o número do id para editar: ")
            if not inputt.isdigit():
                print("> ID inválido. Digite apenas números.")
                return
            id_valor = int(inputt)

            # Verificação de existência do ID na tabela correspondente
            tabela = {
                "1": "Livro",
                "2": "Editora",
                "3": "Autor",
                "4": "Cliente"
            }.get(tipo)
            if not tabela:
                print("> Tipo inválido.")
                return

            if not banco_de_dado.Existe_dado_na_tabela(tabela, f"id_{tabela.lower()} = {id_valor}"):
                print(f"> ID {id_valor} não encontrado na tabela {tabela}.")
                return
        else:
            id_valor = 0

        if tipo == "1":
            banco_de_dado.cadastrar_livro(edicao, id_valor)
        elif tipo == "2":
            banco_de_dado.cadastrar_Publicadora(edicao, id_valor)
        elif tipo == "3":
            banco_de_dado.cadastrar_autor(edicao, id_valor)
        elif tipo == "4":
            banco_de_dado.cadastrar_cliente(edicao, id_valor)
    except Exception as e:
        print(f"> Erro inesperado: {e}")

def Cadastrar_itens(edicao=False):
    Cadastro = {
        "1": "Cadastrar Livros" if not edicao else "Editar Livro",
        "2": "Cadastrar Publicadora" if not edicao else "Editar Publicadora",
        "3": "Cadastrar Autor" if not edicao else "Editar Autor",
        "4": "Cadastrar Usuario" if not edicao else "Editar Usuario"
    }

    while True:
        utils.clean_terminal()
        respota = cli.exibir_cli(Cadastro)

        if respota == str(0):
            main()
            break
        elif respota in {"1", "2", "3", "4"}:
            tratar_cadastro_ou_edicao(respota, edicao)
        pass
    pass

def excluir():
    import data_base as db

    opcoes = {
        "1": "Livro",
        "2": "Editora",
        "3": "Autor",
        "4": "Cliente"
    }
    escolha = cli.exibir_cli(opcoes, saida_nome="Cancelar")
    if escolha == "0":
        return

    id_item = input(f"Digite o ID do(a) {opcoes[escolha]} para excluir: ").strip()
    if not id_item.isdigit():
        print("> ID inválido. Digite apenas números.")
        return
    id_item = int(id_item)

    try:
        if escolha == "1":
            db.Limpar_relacao("Livro_autor", f"id_livro = {id_item}")
            db.Limpar_relacao("Livro_editora", f"id_livro = {id_item}")
            db.Limpar_relacao("Livro", f"id_livro = {id_item}")
            print("> Livro e relações removidos com sucesso.")
        elif escolha == "2":
            db.Limpar_relacao("Livro_editora", f"id_editora = {id_item}")
            db.Limpar_relacao("Editora_endereco", f"id_editora = {id_item}")
            db.Limpar_relacao("Editora", f"id_editora = {id_item}")
            print("> Editora e relações removidas com sucesso.")
        elif escolha == "3":
            livros_autor = db.Ler_dados_da_tabela("Livro_autor", "id_livro", f"id_autor = {id_item}")
            for livro in livros_autor:
                id_livro = livro[0]
                autores = db.Ler_dados_da_tabela("Livro_autor", "COUNT(*)", f"id_livro = {id_livro}")
                if autores and autores[0][0] == 1:
                    db.Limpar_relacao("Livro_autor", f"id_livro = {id_livro}")
                    db.Limpar_relacao("Livro_editora", f"id_livro = {id_livro}")
                    db.Limpar_relacao("Livro", f"id_livro = {id_livro}")
                    print(f"> Livro {id_livro} removido (autor único).")
                else:
                    db.Limpar_relacao("Livro_autor", f"id_livro = {id_livro} AND id_autor = {id_item}")
            db.Limpar_relacao("Autor", f"id_autor = {id_item}")
            print("> Autor e relações removidas com sucesso.")
        elif escolha == "4":
            db.Limpar_relacao("Endereco_cliente", f"id_cliente = {id_item}")
            db.Limpar_relacao("Cliente", f"id_cliente = {id_item}")
            print("> Cliente e relações removidas com sucesso.")
        else:
            print("> Opção inválida.")
    except Exception as e:
        print(f"> Erro inesperado ao excluir: {e}")
def criar_padrao():
    criar_bd_padrao.criar_banco_padrao()
    utils.clean_terminal()
    pass

main()