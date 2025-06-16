import classes as cla
import data_base as db
import utils
#Aqui contem dados que vai exibir como Cli, recebe um dicionario que converte como um cli
def exibir_cli(escolhas_disponiveis, saida_nome="Voltar"):
    escolhas_disponiveis["0"] = saida_nome

    # Exibir os textos do CLI
    for key, value in escolhas_disponiveis.items():
        print(f"{key}: {value}")

    escolha_user = input("\nInsira o comando: ")

    # Determinar se o usuário selecionou corretamente
    if escolha_user in escolhas_disponiveis:
        return escolha_user
    else:
        print("Opção inválida")
        return exibir_cli(escolhas_disponiveis)

def cli_bool(mensagem="Tem certeza que quer continuar?"):
    mensagem += "(S/N)"
    while True:
        resposta = input(mensagem).strip().upper()
        if resposta == "S":
            return True
        elif resposta == "N":
            return False
        else:
            print("Por favor, responda apenas com 'S' ou 'N'.")

def cadastrar_livros_cli():

    print("Cadastrar livros".upper())

    # Tratamento para nome do livro
    while True:
        nome_livro = input("- Nome do livro: ").strip()
        if nome_livro:
            break
        print("> Erro: O nome do livro não pode estar vazio.")
    utils.clean_terminal()

    print("Inserir autores".upper())
    autores = []
    
    while True:
        try:
            entrada = input("\n- Inserir 0 para parar\n-- Autor id {}: ".format(len(autores) + 1))
            id_autor = int(entrada) if entrada.isdigit() else -1
            
            if id_autor == 0:
                if not autores:
                    print("> Erro: Adicione pelo menos 1 autor")
                    continue
                break
                
            if id_autor < 1:
                print("> Erro: ID deve ser positivo")
                continue
                
            if db.Existe_dado_na_tabela("Autor", f"id_autor = {id_autor}"):
                resultado = db.Ler_dados_da_tabela("Autor", "nome_autor", f"id_autor = {id_autor}")
                nome_autor = resultado[0][0] if resultado else "Desconhecido"
                print(f"> Autor adicionado: {nome_autor}")
                autores.append(id_autor)
                print("> IDs dos autores:", autores)
            else:
                print("> Erro: Autor não encontrado. Tente outro ID.")
                
        except ValueError:
            print("> Erro: Digite um número válido para o ID")
        except Exception as e:
            print(f"> Erro inesperado: {str(e)}")

    utils.clean_terminal()

    # Tratamento para editora
    tem_editora = cli_bool("\n- O livro tem uma editora?")
    
    editora_id = None
    if tem_editora:
        while True:
            try:
                editora_id = int(input("ID da editora: "))
                if db.Existe_dado_na_tabela("Editora", f"id_editora = {editora_id}"):
                    resultado = db.Ler_dados_da_tabela("Editora", "nome_editora", f"id_editora = {editora_id}")
                    nome_editora = resultado[0][0] if resultado else "Desconhecida"
                    print(f"> Editora selecionada: {nome_editora}")
                    break
                print("> Erro: Editora não encontrada. Tente outro ID.")
            except ValueError:
                print("> Erro: Digite um número válido para o ID")
            except Exception as e:
                print(f"> Erro inesperado: {str(e)}")

    utils.clean_terminal()

    # Tratamento para número de páginas
    while True:
        try:
            paginas = int(input("- Quantidade de páginas: "))
            if paginas > 0:
                break
            print("> Erro: O número de páginas deve ser positivo")
        except ValueError:
            print("> Erro: Digite um número válido para as páginas")
    utils.clean_terminal()

    # Tratamento para data de publicação
    data = cla.Data_calendario()
    print("- Data de publicação")
    
    while True:
        try:
            ano = int(input("# Ano (YYYY): "))
            if 1000 <= ano <= 9999:
                data.set_year(ano)
                break
            print("> Erro: Ano deve estar entre 1000 e 9999")
        except ValueError:
            print("> Erro: Digite um ano válido")
    
    while True:
        try:
            mes = int(input("Mês (1-12): "))
            if 1 <= mes <= 12:
                data.set_month(mes)
                break
            print("> Erro: Mês deve estar entre 1 e 12")
        except ValueError:
            print("> Erro: Digite um mês válido")
    
    while True:
        try:
            dia = int(input("Dia: "))
            if 1 <= dia <= 31:  # Validação básica, poderia ser mais precisa
                data.set_day(dia)
                break
            print("> Erro: Dia deve estar entre 1 e 31")
        except ValueError:
            print("> Erro: Digite um dia válido")

    print("Data:", data.data_sql)
    utils.clean_terminal()

    try:
        livro = cla.Insercao_livro(nome_livro, paginas, autores, editora_id, data.data_sql)
        print("> Livro cadastrado com sucesso!")
        return livro
    except Exception as e:
        print(f"> Erro ao cadastrar livro: {str(e)}")
        return None

def publicadora_cli():
    print("\n" + "="*50)
    print("CADASTRAR EDITORA".center(50))
    print("="*50 + "\n")

    # Coleta informações básicas da editora
    while True:
        nome_editora = input("- Nome da editora: ").strip()
        if nome_editora:
            break
        print("> Erro: O nome da editora não pode estar vazio")

    # Coleta informações de endereço
    print("\n" + "-"*50)
    print("ENDEREÇO DA EDITORA".center(50))
    print("-"*50 + "\n")

    while True:
        try:
            cep = input("- CEP (apenas números ou formato XXXXX-XXX): ").strip()
            cidade = input("- Cidade: ").strip()
            bairro = input("- Bairro: ").strip()
            rua = input("- Rua: ").strip()
            estado = input("- Estado (sigla): ").strip().upper()
            numero = input("- Número: ").strip()

            endereco = cla.Endereco(
                CEP=cep,
                Cidade=cidade,
                Bairro=bairro,
                Rua=rua,
                Estado=estado,
                Numero=numero
            )

            # Mostra confirmação
            print("\n" + "="*50)
            print("CONFIRMAÇÃO DE CADASTRO".center(50))
            print("="*50 + "\n")
            print(f"Nome da Editora: {nome_editora}")
            print("\nEndereço:")
            print(endereco.formatado())

            # Confirmação final
            if cli_bool("\nConfirmar cadastro? (S/N): "):
                # Aqui você incluiria a lógica para salvar no banco de dados
                print("\n> Editora cadastrada com sucesso!")
                
                return {
                    'nome_editora': nome_editora,
                    'endereco': endereco.to_dict()
                }
            else:
                print("\n> Cadastro cancelado")
                if not cli_bool("Deseja tentar novamente? (S/N): "):
                    return None
                print("\n" + "="*50)
                print("NOVA TENTATIVA DE CADASTRO".center(50))
                print("="*50 + "\n")

        except ValueError as e:
            print(f"\n> Erro: {str(e)}")
            print("> Por favor, corrija os dados e tente novamente\n")
        except Exception as e:
            print(f"\n> Erro inesperado: {str(e)}")
            if not cli_bool("Deseja tentar novamente? (S/N): "):
                return None