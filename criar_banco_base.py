import data_base as bd
import os.path
def criar_banco_padrao():
    if os.path.isfile(bd.standart_path):
        print("Banco padrão já existe")
        return
    bd.Criar_banco(bd.standart_path)
    bd.Criar_table(
    "Editora",
    "id_editora INTEGER PRIMARY KEY, nome_editora TEXT NOT NULL"
    )

    bd.Criar_table(
        "Endereco",
        "id_endereco INTEGER PRIMARY KEY, CEP TEXT, Cidade TEXT, Bairro TEXT, Rua TEXT, Estado TEXT, Numero TEXT"
    )

    bd.Criar_table(
        "Editora_endereco",
        "id_editora INTEGER UNIQUE, id_endereco INTEGER, " +
        "FOREIGN KEY (id_editora) REFERENCES Editora(id_editora), " +
        "FOREIGN KEY (id_endereco) REFERENCES Endereco(id_endereco)"
    )

    bd.Criar_table(
        "Cliente",
        "id_cliente INTEGER PRIMARY KEY, nome TEXT, sexo_cliente TEXT, aniversario DATE, " +
        "email TEXT, telefone TEXT, CPF TEXT"
    )

    bd.Criar_table(
        "Endereco_cliente",
        "id_cliente INTEGER, id_endereco INTEGER, " +
        "FOREIGN KEY (id_cliente) REFERENCES Cliente(id_cliente), " +
        "FOREIGN KEY (id_endereco) REFERENCES Endereco(id_endereco)"
    )

    bd.Criar_table(
        "Autor",
        "id_autor INTEGER PRIMARY KEY, nome_autor TEXT, genero_autor TEXT, nascimento DATE"
    )

    bd.Criar_table(
        "Livro",
        "id_livro INTEGER PRIMARY KEY, nome TEXT, lancamento DATE, paginas INTEGER"
    )

    bd.Criar_table(
        "Livro_editora",
        "id_livro INTEGER UNIQUE, id_editora INTEGER, " +
        "FOREIGN KEY (id_livro) REFERENCES Livro(id_livro), " +
        "FOREIGN KEY (id_editora) REFERENCES Editora(id_editora)"
    )

    bd.Criar_table(
        "Livro_autor",
        "id_livro INTEGER, id_autor INTEGER, " +
        "PRIMARY KEY (id_livro, id_autor), " +
        "FOREIGN KEY (id_livro) REFERENCES Livro(id_livro), " +
        "FOREIGN KEY (id_autor) REFERENCES Autor(id_autor)"
    )

    bd.Criar_table(
        "Emprestimo",
        "id_emprestimo INTEGER PRIMARY KEY, id_livro INTEGER, id_cliente INTEGER, " +
        "data_emprestimo DATE, data_devolucao DATE, " +
        "FOREIGN KEY (id_livro) REFERENCES Livro(id_livro), " +
        "FOREIGN KEY (id_cliente) REFERENCES Cliente(id_cliente)"
    )
    preencher_banco_padrao()
    pass

def preencher_banco_padrao():
    # Endereco
    bd.Adicionar_dado_a_table_ESPECIFICO(
        "Endereco",
        ["CEP", "Cidade", "Bairro", "Rua", "Estado", "Numero"],
        ["12345-678", "Cidade A", "Centro", "Rua Alpha", "SP", "100"]
    )
    bd.Adicionar_dado_a_table_ESPECIFICO(
        "Endereco",
        ["CEP", "Cidade", "Bairro", "Rua", "Estado", "Numero"],
        ["98765-432", "Cidade B", "Bairro B", "Rua Beta", "RJ", "200"]
    )

    # Editora
    bd.Adicionar_dado_a_table_ESPECIFICO(
        "Editora",
        ["nome_editora"],
        ["Editora Alpha"]
    )
    bd.Adicionar_dado_a_table_ESPECIFICO(
        "Editora",
        ["nome_editora"],
        ["Editora Beta"]
    )

    # Editora_endereco
    bd.Adicionar_dado_a_table_ESPECIFICO(
        "Editora_endereco",
        ["id_editora", "id_endereco"],
        [1, 1]
    )
    bd.Adicionar_dado_a_table_ESPECIFICO(
        "Editora_endereco",
        ["id_editora", "id_endereco"],
        [2, 2]
    )

    # Cliente
    bd.Adicionar_dado_a_table_ESPECIFICO(
        "Cliente",
        ["nome", "sexo_cliente", "aniversario", "email", "telefone", "CPF"],
        ["João Silva", "M", "1990-01-01", "joao@email.com", "11999999999", "123.456.789-00"]
    )
    bd.Adicionar_dado_a_table_ESPECIFICO(
        "Cliente",
        ["nome", "sexo_cliente", "aniversario", "email", "telefone", "CPF"],
        ["Maria Souza", "F", "1985-05-15", "maria@email.com", "11988888888", "987.654.321-00"]
    )

    # Endereco_cliente
    bd.Adicionar_dado_a_table_ESPECIFICO(
        "Endereco_cliente",
        ["id_cliente", "id_endereco"],
        [1, 1]
    )
    bd.Adicionar_dado_a_table_ESPECIFICO(
        "Endereco_cliente",
        ["id_cliente", "id_endereco"],
        [2, 2]
    )

    # Autor
    bd.Adicionar_dado_a_table_ESPECIFICO(
        "Autor",
        ["nome_autor", "genero_autor", "nascimento"],
        ["Autor Um", "M", "1970-01-01"]
    )
    bd.Adicionar_dado_a_table_ESPECIFICO(
        "Autor",
        ["nome_autor", "genero_autor", "nascimento"],
        ["Autora Dois", "F", "1980-02-02"]
    )

    # Livro
    bd.Adicionar_dado_a_table_ESPECIFICO(
        "Livro",
        ["nome", "lancamento", "paginas"],
        ["Livro A", "2020-01-01", 200]
    )
    bd.Adicionar_dado_a_table_ESPECIFICO(
        "Livro",
        ["nome", "lancamento", "paginas"],
        ["Livro B", "2021-06-15", 350]
    )

    # Livro_editora
    bd.Adicionar_dado_a_table_ESPECIFICO(
        "Livro_editora",
        ["id_livro", "id_editora"],
        [1, 1]
    )
    bd.Adicionar_dado_a_table_ESPECIFICO(
        "Livro_editora",
        ["id_livro", "id_editora"],
        [2, 2]
    )

    # Livro_autor
    bd.Adicionar_dado_a_table_ESPECIFICO(
        "Livro_autor",
        ["id_livro", "id_autor"],
        [1, 1]
    )
    bd.Adicionar_dado_a_table_ESPECIFICO(
        "Livro_autor",
        ["id_livro", "id_autor"],
        [2, 2]
    )

    # Emprestimo
    bd.Adicionar_dado_a_table_ESPECIFICO(
        "Emprestimo",
        ["id_livro", "id_cliente", "data_emprestimo", "data_devolucao"],
        [1, 1, "2024-06-01", "2024-06-15"]
    )
    bd.Adicionar_dado_a_table_ESPECIFICO(
        "Emprestimo",
        ["id_livro", "id_cliente", "data_emprestimo", "data_devolucao"],
        [2, 2, "2024-06-03", "2024-06-17"]
    )


