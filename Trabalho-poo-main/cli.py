import classes as cla
import data_base as db
import utils
import datetime

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

    print("CADASTRAR LIVROS".upper())

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
    
    # Tratamento para quantidade total de exemplares
    while True:
        try:
            quantidade = int(input("- Quantidade total de exemplares: "))
            if quantidade > 0:
                break
            print("> Erro: A quantidade deve ser um número positivo")
        except ValueError:
            print("> Erro: Digite um número válido para a quantidade")
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
            if 1 <= dia <= 31:  # Validação básica, pode ser aprimorada
                data.set_day(dia)
                break
            print("> Erro: Dia deve estar entre 1 e 31")
        except ValueError:
            print("> Erro: Digite um dia válido")

    print("Data:", data.data_sql)
    utils.clean_terminal()

    try:
        # Agora, a instância inclui também a quantidade total de exemplares.
        livro = cla.Insercao_livro(nome_livro, paginas, autores, editora_id, data.data_sql, quantidade)
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

def autor_cli():
    import classes as cla  # Caso não esteja importado no início
    print("\n" + "="*50)
    print("CADASTRAR AUTOR".center(50))
    print("="*50 + "\n")
    
    # Nome
    while True:
        nome = input("- Nome do autor: ").strip()
        if nome:
            break
        print("> Erro: O nome do autor não pode estar vazio")
    
    # Sexo
    while True:
        sexo = input("- Sexo (M/F/NB): ").strip().upper()
        if sexo in ['M', 'F', 'NB']:
            break
        print("> Erro: Digite 'M' para Masculino, 'F' para Feminino ou 'NB' para Não Binário/Não Informado")
    
    # Data de nascimento usando a classe Data_calendario
    print("\n- Data de Nascimento")
    data = cla.Data_calendario()  # valor padrão para criar uma instância
    while True:
        try:
            ano = int(input("  Ano (YYYY): "))
            data.set_year(ano)
            break
        except ValueError:
            print("> Erro: Ano inválido. Digite um número no formato YYYY.")
    
    while True:
        try:
            mes = int(input("  Mês (1-12): "))
            data.set_month(mes)
            break
        except ValueError:
            print("> Erro: Mês inválido. Digite um número entre 1 e 12.")
    
    while True:
        try:
            dia = int(input("  Dia: "))
            data.set_day(dia)
            break
        except ValueError:
            print("> Erro: Dia inválido. Digite um número válido para o dia.")
    
    nascimento = data.data_sql

    # Confirmação dos dados
    print("\n" + "="*50)
    print("CONFIRMAÇÃO DE CADASTRO".center(50))
    print("="*50 + "\n")
    print(f"Nome: {nome}")
    print(f"Sexo: {sexo}")
    print(f"Data de nascimento: {nascimento}")
    
    if cli_bool("\nConfirmar cadastro?"):
        return {
            "nome_autor": nome,
            "sexo": sexo,
            "nascimento": nascimento
        }
    else:
        print("\n> Cadastro cancelado")
        return None

def usuario_cli():

    print("\n" + "="*50)
    print("CADASTRAR USUÁRIO".center(50))
    print("="*50 + "\n")
    
    # Nome do usuário
    while True:
        nome = input("- Nome do usuário: ").strip()
        if nome:
            break
        print("> Erro: O nome não pode estar vazio")
    
    # Sexo
    while True:
        sexo = input("- Sexo (M/F/NB): ").strip().upper()
        if sexo in ['M', 'F', 'NB']:
            break
        print("> Erro: Digite 'M' para Masculino, 'F' para Feminino ou 'NB' para Não Binário/Não Informado")
    
    # Data de nascimento utilizando a classe Data_calendario
    print("\n- Data de Nascimento")
    data = cla.Data_calendario()  # Instância com valor padrão
    while True:
        try:
            ano = int(input("  Ano (YYYY): "))
            data.set_year(ano)
            break
        except ValueError:
            print("> Erro: Ano inválido. Digite um número no formato YYYY.")
    
    while True:
        try:
            mes = int(input("  Mês (1-12): "))
            data.set_month(mes)
            break
        except ValueError:
            print("> Erro: Mês inválido. Digite um número entre 1 e 12.")
    
    while True:
        try:
            dia = int(input("  Dia: "))
            data.set_day(dia)
            break
        except ValueError:
            print("> Erro: Dia inválido. Digite um número válido para o dia.")
    
    nascimento = data.data_sql

    # Email
    while True:
        email = input("- Email: ").strip()
        if "@" in email and "." in email:
            break
        print("> Erro: Email inválido. Tente novamente.")
        
    # Telefone (ex: 11999999999) - apenas números, 10 ou 11 dígitos
    while True:
        telefone = input("- Telefone (ex: 11999999999): ").strip()
        if telefone.isdigit() and len(telefone) in [10, 11]:
            break
        print("> Erro: Telefone inválido. Informe apenas números (10 ou 11 dígitos).")
    
    # CPF: 11 dígitos numéricos
    while True:
        cpf = input("- CPF (apenas números): ").strip()
        if cpf.isdigit() and len(cpf) == 11:
            break
        print("> Erro: CPF inválido. Informe 11 dígitos numéricos.")
    cpf = f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"

    # Endereço (similar ao cadastro de editora)
    print("\n" + "-"*50)
    print("ENDEREÇO DO USUÁRIO".center(50))
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
            
            print("\n" + "="*50)
            print("CONFIRMAÇÃO DE CADASTRO".center(50))
            print("="*50 + "\n")
            print(f"Nome: {nome}")
            print(f"Sexo: {sexo}")
            print(f"Data de nascimento: {nascimento}")
            print(f"Email: {email}")
            print(f"Telefone: {telefone}")
            print(f"CPF: {cpf}")
            print("\nEndereço:")
            print(endereco.formatado())
            
            if cli_bool("\nConfirmar cadastro? "):
                print("\n> Usuário cadastrado com sucesso!")
                return {
                    "nome_usuario": nome,
                    "sexo": sexo,
                    "nascimento": nascimento,
                    "email": email,
                    "telefone": telefone,
                    "cpf": cpf,
                    "endereco": endereco.to_dict()
                }
            else:
                print("\n> Cadastro cancelado")
                if not cli_bool("Deseja tentar novamente? "):
                    return None
                print("\n" + "="*50)
                print("NOVA TENTATIVA DE CADASTRO".center(50))
                print("="*50 + "\n")
        except ValueError as e:
            print(f"\n> Erro: {str(e)}")
            print("> Por favor, corrija os dados e tente novamente\n")
        except Exception as e:
            print(f"\n> Erro inesperado: {str(e)}")
            if not cli_bool("Deseja tentar novamente? "):
                return None
            
def mostrar_todos_os_itens(item):
    db.print_dados(item)
    pass

def emprestimo():
    print("\n" + "="*50)
    print("REALIZAR EMPRÉSTIMO".center(50))
    print("="*50 + "\n")
    
    # Solicitar e validar ID do livro
    while True:
        try:
            id_livro = int(input("Digite o ID do livro: "))
            if not db.Existe_dado_na_tabela("Livro", f"id_livro = {id_livro}"):
                print("> Erro: Livro não encontrado. Tente novamente.")
                continue
            break
        except ValueError:
            print("> Erro: ID inválido. Digite um número válido.")
    
    # Solicitar e validar ID do usuário (Cliente)
    while True:
        try:
            id_usuario = int(input("Digite o ID do usuário: "))
            if not db.Existe_dado_na_tabela("Cliente", f"id_cliente = {id_usuario}"):
                print("> Erro: Usuário não encontrado. Tente novamente.")
                continue
            break
        except ValueError:
            print("> Erro: ID inválido. Digite um número válido.")
    
    # Confirmação do empréstimo
    if cli_bool("\nConfirmar empréstimo? "):
        data_atual = datetime.date.today()
        data_devolucao_date = data_atual + datetime.timedelta(days=7)
        
        data_emprestimo = cla.Data_calendario(data_atual.day, data_atual.month, data_atual.year)
        data_devolucao = cla.Data_calendario(data_devolucao_date.day, data_devolucao_date.month, data_devolucao_date.year)
        
        resultado = {
            "id_livro": id_livro,
            "id_usuario": id_usuario,
            "data_emprestimo": data_emprestimo.data_sql,
            "data_devolucao": data_devolucao.data_sql,
            "data_devolucao_prevista": None,
            "status" : "emprestado"
        }
        
        disponivies = verificar_disponibilidade(id_livro)

        if disponivies <= 0:
            print("Operação cancelada, não há exemplares disponivies")
            return None


        print("\n> Empréstimo realizado com sucesso!")
        print(">> Detalhes do Empréstimo:")
        for chave, valor in resultado.items():
            print(f"{chave}: {valor}")
        
        return resultado
    else:
        print("\n> Empréstimo cancelado")
        return None

def verificar_disponibilidade(id_livro_padrao = None):
    id_livro = None
    perguntar = False

    if id_livro_padrao == None:
        print("\n" + "="*50)
        print("VERIFICAR DISPONIBILIDADE DO LIVRO".center(50))
        print("="*50 + "\n")
        perguntar = True

    if perguntar:
        while True:
            try:
                id_livro = int(input("Digite o ID do livro: "))
                break
            except ValueError:
                print("> Erro: Digite um número válido para o ID")
    else:
        id_livro = id_livro_padrao
    
    # Contar apenas empréstimos ativos (status='emprestado' e não devolvidos)
    resultado_emprestimo = db.Ler_dados_da_tabela(
        "Emprestimo",
        "COUNT(*)",
        f"id_livro = {id_livro} AND status = 'emprestado'"
    )
    emprestados = resultado_emprestimo[0][0] if resultado_emprestimo and resultado_emprestimo[0] else 0
    
    # Recuperar a quantidade total de unidades do livro
    resultado_livro = db.Ler_dados_da_tabela(
        "Livro",
        "unidades_totais",
        f"id_livro = {id_livro}"
    )
    if resultado_livro:
        unidades_totais = resultado_livro[0][0]
    else:
        print("> Erro: Livro não encontrado na base de dados.")
        return None

    disponivel = unidades_totais - emprestados
    disponivel = disponivel if disponivel >= 0 else 0

    # Recupera o nome do livro para exibição
    resultado_nome = db.Ler_dados_da_tabela(
        "Livro",
        "nome",
        f"id_livro = {id_livro}"
    )
    nome_livro = resultado_nome[0][0] if resultado_nome else "Desconhecido"

    print(f"\n> Livro ID {id_livro} - {nome_livro}:")
    print(f"   Unidades Totais: {unidades_totais}")
    print(f"   Emprestadas: {emprestados}")
    print(f"   Disponíveis: {disponivel}")
    
    return disponivel


def devolver_livro():
    print("\n" + "="*50)
    print("DEVOLVER LIVRO".center(50))
    print("="*50 + "\n")

    while True:
        try:
            id_livro = int(input("Digite o ID do livro a ser devolvido: "))
            break
        except ValueError:
            print("> Erro: Digite um número válido para o ID do livro.")

    while True:
        try:
            id_usuario = int(input("Digite o ID do usuário que realizou o empréstimo: "))
            break
        except ValueError:
            print("> Erro: Digite um número válido para o ID do usuário.")

    # Verificar se existe um empréstimo com status "emprestado" para o livro e usuário informados.
    emprestimos = db.Ler_dados_da_tabela(
        "Emprestimo",
        "*",
        f"id_livro = {id_livro} AND id_cliente = {id_usuario} AND status = 'emprestado'"
    )
    if not emprestimos:
        print("> Erro: Nenhum empréstimo encontrado para esse livro e usuário com status 'emprestado'.")
        return None

    if not cli_bool("\nConfirmar devolução? "):
        print("\n> Operação cancelada.")
        return None

    # Data de processamento (data da devolução) utilizando a classe Data_calendario
    data_atual = datetime.date.today()
    data_devolucao = cla.Data_calendario(data_atual.day, data_atual.month, data_atual.year)

    # Atualiza o status do empréstimo e registra a data de devolução
    db.Alterar_table(
        "Emprestimo",
        {"status": "devolvido", "data_retornado": data_devolucao.data_sql},
        f"id_livro = {id_livro} AND id_cliente = {id_usuario} AND status = 'emprestado'"
    )

    resultado = {
        "id_livro": id_livro,
        "id_usuario": id_usuario,
        "status": "devolvido",
        "data_devolucao": data_devolucao.data_sql
    }

    print("Detalhes da devolução:")
    for chave, valor in resultado.items():
        print(f"{chave}: {valor}")
    
    return resultado
    pass

def relatorio_disponibilidade():
    print("\n" + "="*50)
    print("RELATÓRIO DE DISPONIBILIDADE DE LIVROS".center(50))
    print("="*50 + "\n")
    
    livros = db.Ler_dados_da_tabela("Livro", "*")
    if not livros:
        print("> Nenhum livro cadastrado.")
        return

    for livro in livros:
        id_livro = livro[0]
        nome = livro[1]
        unidades_totais = livro[4]
        # Consulta a quantidade de empréstimos com status 'emprestado'
        resultado = db.Ler_dados_da_tabela("Emprestimo", "COUNT(*)", f"id_livro = {id_livro} AND status = 'emprestado'")
        emprestados = resultado[0][0] if resultado and resultado[0] else 0
        disponivel = unidades_totais - emprestados
        
        print(f"ID: {id_livro} | Livro: {nome}")
        print(f"Total de Unidades: {unidades_totais}")
        print(f"Emprestadas: {emprestados} | Disponíveis: {disponivel}")
        print("-"*50)

def relatorio_emprestimos():
    print("\n" + "="*50)
    print("RELATÓRIO DE EMPRÉSTIMOS ATIVOS".center(50))
    print("="*50 + "\n")
    
    # Consulta todos os empréstimos com status 'emprestado'
    emprestimos = db.Ler_dados_da_tabela("Emprestimo", "*", "status = 'emprestado'")
    if not emprestimos:
        print("> Nenhum empréstimo ativo encontrado.")
        return

    # Organiza os empréstimos por usuário
    emprestimos_por_cliente = {}
    for emp in emprestimos:
        # Assumindo: índice 0: id_emprestimo, 1: id_livro, 2: id_cliente,
        # 3: status, 4: data_retornado, 5: data_emprestimo, 6: data_devolucao
        id_cliente = emp[2]
        if id_cliente not in emprestimos_por_cliente:
            emprestimos_por_cliente[id_cliente] = []
        emprestimos_por_cliente[id_cliente].append(emp)
    
    # Exibe o relatório
    for id_cliente, loans in emprestimos_por_cliente.items():
        print(f"Usuário ID: {id_cliente}")
        for emp in loans:
            id_livro = emp[1]
            data_emprestimo = emp[5]
            data_devolucao = emp[6]
            print(f"    Livro ID: {id_livro} | Empréstimo: {data_emprestimo} | Devolução Prevista: {data_devolucao}")
        print("-"*50)

def relatorio_atrasos():
    import datetime
    import data_base as db

    print("\n" + "="*50)
    print("RELATÓRIO DE ATRASOS".center(50))
    print("="*50 + "\n")
    
    # Data atual para verificar atrasos de livros não devolvidos
    data_atual = datetime.date.today()
    
    # Consulta todos os empréstimos (devolvidos e não devolvidos)
    registros = db.Ler_dados_da_tabela("Emprestimo", "*")
    
    if not registros:
        print("> Nenhum empréstimo encontrado.")
        return

    encontrou_atraso = False
    for reg in registros:
        try:
            data_devolucao_prevista = datetime.datetime.strptime(reg[6], "%Y-%m-%d").date()
            
            # Caso 1: Livro já devolvido
            if reg[4] is not None:  # data_retornado existe
                data_retorno = datetime.datetime.strptime(reg[4], "%Y-%m-%d").date()
                if data_retorno > data_devolucao_prevista:
                    atraso = (data_retorno - data_devolucao_prevista).days
                    print(f"Empréstimo ID: {reg[0]} [DEVOLVIDO COM ATRASO]")
                    print(f"    Livro ID: {reg[1]} | Usuário ID: {reg[2]}")
                    print(f"    Data prevista: {reg[6]}")
                    print(f"    Data retornado: {reg[4]}")
                    print(f"    Atraso: {atraso} dia(s)")
                    print("-" * 50)
                    encontrou_atraso = True
            
            # Caso 2: Livro ainda não devolvido e atrasado
            elif data_atual > data_devolucao_prevista:
                atraso = (data_atual - data_devolucao_prevista).days
                print(f"Empréstimo ID: {reg[0]} [AINDA NÃO DEVOLVIDO]")
                print(f"    Livro ID: {reg[1]} | Usuário ID: {reg[2]}")
                print(f"    Data prevista: {reg[6]}")
                print(f"    Atraso atual: {atraso} dia(s)")
                print("-" * 50)
                encontrou_atraso = True

        except Exception as e:
            print(f"> Erro ao processar registro {reg[0]}: {str(e)}")
            continue

    if not encontrou_atraso:
        print("> Nenhum atraso encontrado.")