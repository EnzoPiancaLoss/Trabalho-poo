import sqlite3
import classes as cla
import utils 
import cli
standart_path = "Biblioteca.db"

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
    try:
        colunas = f"({', '.join(nome_chaves)})"
        placeholders = ', '.join(['?'] * len(valores_chaves))
        

        command = f"INSERT INTO {table} {colunas} VALUES ({placeholders})"

        # print("> Comando:", command)
        # print("> Valores:", valores_chaves)
        
        cursor.execute(command, valores_chaves)
        conn.commit()
        print("> Inserção bem-sucedida.")

    except sqlite3.Error as e:
        print("> Erro ao inserir:", e)
    finally:
        conn.close()

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

        print("--Resultados--")
        for linha in resultados:
            print(linha)
        print("--------------")

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


def cadastrar_livro(table = ''):
    
    classe_criada = cli.cadastrar_livros_cli()

    print(classe_criada.print_dados())

    classe_criada.Salvar_para_sql()
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






# Adicionar_dado_a_table_ESPECIFICO(
#     "Livros", 
#     ["nome", "lancamento"], 
#     ["Livro A", "2020-01-01"]
# )


# table()
# Criar_table("Livros", "id_livro INTEGER PRIMARY KEY, nome TEXT NOT NULL, lancamento DATE","tes")
#Criar_banco()
#Criar_table("Livros", "id_livro INTEGER PRIMARY KEY, nome TEXT NOT NULL, lancamento DATE")
# Criar_table("Livros2", "id_livro INTEGER PRIMARY KEY, nome TEXT NOT NULL, lancamento DATE")