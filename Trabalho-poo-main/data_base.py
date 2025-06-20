import sqlite3
import classes as cla
import utils 
import cli
standart_path = "Biblioteca.db"


def print_dados(table, path = standart_path):
    conn = sqlite3.connect(path)
    cursor = conn.cursor()

    # Suponha que temos uma tabela chamada 'clientes' com uma coluna 'nome'
    cursor.execute(f"SELECT * FROM {table}")  # Substitua 'nome' pelo nome da coluna desejada

    # Buscar todos os resultados
    resultados = cursor.fetchall()

    # Imprimir cada valor da coluna
    for linha in resultados:
        print(linha)  #


#Essa função vai criar uma table
def Criar_banco(nome_banco_de_dados = standart_path):
    #O primeiro try vai indentificar se o banco pode ser criado com o caminho dado
    try:
        if not nome_banco_de_dados.endswith(".db"):
            print(f"> Caminho do banco de dados invalido: {nome_banco_de_dados}")
            return
        conn = sqlite3.connect(nome_banco_de_dados)
        cursor = conn.cursor()
        results = cursor.fetchall()
        #print(results)
        pass
    except NameError:
        print(NameError)
        return
    pass

#Cria uma table
def Criar_table(Nome_table, chaves_comando, database_a_usar = standart_path):
    database_a_usar = sqlite3.connect(database_a_usar)
    cursor = database_a_usar.cursor()
    try:
        command = f"""CREATE TABLE IF NOT EXISTS {Nome_table} ( {chaves_comando});"""
        cursor.execute(command)
        results = cursor.fetchall()
        #print(results)
    except NameError:
        print(NameError)
        print("> Erro, chaves_comando para cirar os valores da table está errado!")
        return
        pass
    pass
    

def Adicionar_dado_a_table_ESPECIFICO(table, nome_chaves, valores_chaves, database=standart_path):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    new_id = None
    try:
        colunas = f"({', '.join(nome_chaves)})"
        placeholders = ', '.join(['?'] * len(valores_chaves))
        command = f"INSERT INTO {table} {colunas} VALUES ({placeholders})"
        cursor.execute(command, valores_chaves)
        conn.commit()
        new_id = cursor.lastrowid
        print("> Inserção bem-sucedida.")
    except sqlite3.Error as e:
        print("> Erro ao inserir:", e)
    finally:
        conn.close()
    return new_id

def Alterar_table(table, coluna_valor, condicao, database=standart_path):
    """
    Altera dados em uma tabela existente
    
    Parâmetros:
    table (str): Nome da tabela
    coluna_valor (dict): Dicionário com colunas e novos valores {coluna: valor}
    condicao (str): Condição WHERE para identificar o registro (ex: "id = 1")
    database (str): Caminho do banco de dados (opcional)
    """
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    try:
        # Prepara os valores para atualização
        sets = []
        valores = []
        for coluna, valor in coluna_valor.items():
            sets.append(f"{coluna} = ?")
            valores.append(valor)
        
        valores = tuple(valores)
        set_clause = ", ".join(sets)
        
        command = f"UPDATE {table} SET {set_clause} WHERE {condicao}"
        
        # print("Comando:", command)
        # print("Valores:", valores)
        
        cursor.execute(command, valores)
        conn.commit()
        print("> Atualização bem-sucedida.")
        
    except sqlite3.Error as e:
        print("> Erro ao atualizar:", e)
    finally:
        conn.close()

def Ler_dados_da_tabela(tabela, colunas="*", condicao=None, database=standart_path):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    try:
        query = f"SELECT {colunas} FROM {tabela}"
        if condicao:
            query += f" WHERE {condicao}"
        print("> Consulta:", query)

        cursor.execute(query)
        resultados = cursor.fetchall()

        # print("--Resultados--")
        # for linha in resultados:
        #     print(linha)
        # print("--------------")

        return resultados

    except sqlite3.Error as e:
        print("> Erro ao ler dados:", e)
        return []
    finally:
        conn.close()
    #Ler_dados_da_tabela("Livro",colunas="nome")

def Existe_dado_na_tabela(tabela, condicao, database=standart_path):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    try:
        query = f"SELECT 1 FROM {tabela} WHERE {condicao} LIMIT 1"
        print("> Consulta:", query)

        cursor.execute(query)
        resultado = cursor.fetchone()

        return resultado is not None

    except sqlite3.Error as e:
        print("> Erro ao verificar dado:", e)
        return False
    finally:
        conn.close()


def cadastrar_livro(edicao=False, id_pronto=0):
    classe_criada = cli.cadastrar_livros_cli()

    print(classe_criada.print_dados())

    if cli.cli_bool():
        if edicao:
            # Atualiza o livro existente
            classe_criada.Salvar_para_sql(edicao=True, id_pronto=id_pronto)
        else:
            # Cadastro normal
            classe_criada.Salvar_para_sql()
    else:
        print("> Operação cancelada")
        pass


def cadastrar_Publicadora(edicao=False, id_pronto=0):
    resultado = cli.publicadora_cli()
    if edicao and id_pronto:
        # Atualiza a publicadora existente
        Alterar_table(
            "Editora",
            {"nome_editora": resultado["nome_editora"]},
            f"id_editora = {id_pronto}"
        )
        # Atualiza endereço (você pode querer buscar o id_endereco relacionado e atualizar)
        # Exemplo: Atualiza todos os endereços ligados a essa editora
        enderecos = Ler_dados_da_tabela("Editora_endereco", "id_endereco", f"id_editora = {id_pronto}")
        if enderecos:
            for endereco_id in enderecos:
                Alterar_table(
                    "Endereco",
                    resultado["endereco"],
                    f"id_endereco = {endereco_id[0]}"
                )
        print("> Publicadora atualizada com sucesso!")
    else:
        publisher_id = Adicionar_dado_a_table_ESPECIFICO(
            "Editora",
            ["nome_editora"],
            [resultado["nome_editora"]]
        )
        endereco_id = Adicionar_dado_a_table_ESPECIFICO(
            "Endereco",
            ["CEP", "Cidade", "Bairro", "Rua", "Estado", "Numero"],
            [
                resultado["endereco"]["cep"],
                resultado["endereco"]["cidade"],
                resultado["endereco"]["bairro"],
                resultado["endereco"]["rua"],
                resultado["endereco"]["estado"],
                resultado["endereco"]["numero"]
            ]
        )
        Adicionar_dado_a_table_ESPECIFICO(
            "Editora_endereco",
            ["id_editora", "id_endereco"],
            [publisher_id, endereco_id]
        )
        print(f"> ID da publicadora criada: {publisher_id}")
        print(f"> ID do endereco criada: {endereco_id}")
        print("> Data base criada")
    
    pass
    

def cadastrar_autor(edicao=False, id_pronto=0):
    resultado = cli.autor_cli()
    if edicao and id_pronto:
        Alterar_table(
            "Autor",
            {"nome_autor": resultado["nome_autor"], "genero_autor": resultado["sexo"], "nascimento": resultado["nascimento"]},
            f"id_autor = {id_pronto}"
        )
        print("> Autor atualizado com sucesso!")
    else:
        Adicionar_dado_a_table_ESPECIFICO(
            "Autor",
            ["nome_autor", "genero_autor", "nascimento"],
            [resultado["nome_autor"], resultado["sexo"], resultado["nascimento"]]
        )
        print("> Cadastro terminado")
    pass

def cadastrar_cliente(edicao=False, id_pronto=0):
    resultado = cli.usuario_cli()
    if edicao and id_pronto:
        Alterar_table(
            "Cliente",
            {
                "nome": resultado["nome_usuario"],
                "sexo_cliente": resultado["sexo"],
                "aniversario": resultado["nascimento"],
                "email": resultado["email"],
                "telefone": resultado["telefone"],
                "CPF": resultado["cpf"]
            },
            f"id_cliente = {id_pronto}"
        )
        # Atualiza endereço (busque o id_endereco relacionado e atualize)
        enderecos = Ler_dados_da_tabela("Endereco_cliente", "id_endereco", f"id_cliente = {id_pronto}")
        if enderecos:
            for endereco_id in enderecos:
                Alterar_table(
                    "Endereco",
                    resultado["endereco"],
                    f"id_endereco = {endereco_id[0]}"
                )
        print("> Cliente atualizado com sucesso!")
    else:
        cliente_id = Adicionar_dado_a_table_ESPECIFICO(
            "Cliente",
            ["nome", "sexo_cliente", "aniversario", "email", "telefone", "CPF"],
            [resultado["nome_usuario"], resultado["sexo"], resultado["nascimento"], resultado["email"], resultado["telefone"], resultado["cpf"]]
        )
        endereco_id = Adicionar_dado_a_table_ESPECIFICO(
            "Endereco",
            ["CEP", "Cidade", "Bairro", "Rua", "Estado", "Numero"],
            [
                resultado["endereco"]["cep"],
                resultado["endereco"]["cidade"],
                resultado["endereco"]["bairro"],
                resultado["endereco"]["rua"],
                resultado["endereco"]["estado"],
                resultado["endereco"]["numero"]
            ]
        )
        Adicionar_dado_a_table_ESPECIFICO(
            "Endereco_cliente",
            ["id_cliente", "id_endereco"],
            [cliente_id, endereco_id]
        )
        print("> Adicao concluida")
    pass


def Limpar_relacao(tabela, condicao, database=standart_path):
    import sqlite3
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    try:
        cursor.execute(f"DELETE FROM {tabela} WHERE {condicao}")
        conn.commit()
    finally:
        conn.close()

# utils.clean_terminal()
    # Adicionar_dado_a_table_ESPECIFICO(
    #     "Livro",
    #     ["nome", "lancamento", "paginas"],
    #     ["Livro A", "2020-01-01", 200]
    # )
    pass
    # Exemplo de uso:
    # Alterar_table(
    #     "Livro",
    #     {"nome": "Novo Nome", "lancamento": "2023-01-01"},
    #     "id_livro = 1"
    # )



# table()
# Criar_table("Livros", "id_livro INTEGER PRIMARY KEY, nome TEXT NOT NULL, lancamento DATE","tes")
#Criar_banco()
#Criar_table("Livros", "id_livro INTEGER PRIMARY KEY, nome TEXT NOT NULL, lancamento DATE")
# Criar_table("Livros2", "id_livro INTEGER PRIMARY KEY, nome TEXT NOT NULL, lancamento DATE")