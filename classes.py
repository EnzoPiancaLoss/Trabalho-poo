import datetime
import data_base
class Insercao_livro():
    def __init__(self, nome, paginas, autores_id, publicadora_id, lancamento):
        self.nome = nome
        self.pag = paginas
        self.autores = autores_id
        self.editora = publicadora_id
        self.lancamento = lancamento
        pass

    def print_dados(self):
        """Exibe todos os dados do livro formatados"""
        print("\n>> Dados do Livro:")
        print(f">> Nome: {self.nome}")
        print(f">> Número de páginas: {self.pag}")
        print(f">> ID do Autor: {self.autores}")
        print(f">> ID da Editora: {self.editora}")
        print(f">> Data de Lançamento: {self.lancamento}")

    def Salvar_para_sql(self):
        # 1. Inserir o livro
        data_base.Adicionar_dado_a_table_ESPECIFICO(
            "Livro", 
            ["nome", "lancamento", "paginas"], 
            [self.nome, self.lancamento, self.pag]
        )
        # 2. Buscar id do livro recém-inserido (assumindo que nome + lançamento são únicos)
        resultado = data_base.Ler_dados_da_tabela(
            "Livro", "id_livro", 
            f"nome = '{self.nome}' AND lancamento = '{self.lancamento}'"
        )
        if not resultado:
            print("> Erro: livro não encontrado após inserção.")
            return
        id_livro = resultado[0][0]

        # 3. Inserir cada autor
        for id_autor in self.autores:
            data_base.Adicionar_dado_a_table_ESPECIFICO(
                "Livro_autor",
                ["id_livro", "id_autor"],
                [id_livro, id_autor]
            )

        # 4. Inserir a editora (se houver)
        if self.editora:
            data_base.Adicionar_dado_a_table_ESPECIFICO(
                "Livro_editora",
                ["id_livro", "id_editora"],
                [id_livro, self.editora]
            )

        print("> Livro e relações inseridos com sucesso.")

class Data_calendario:
    def __init__(self, dia=30, mes=11, ano=2000):
        self._validar_data(dia, mes, ano)
        self.ano = ano
        self.mes = mes
        self.dia = dia
    
    @staticmethod
    def _validar_data(dia, mes, ano):
        try:
            datetime.date(ano, mes, dia)  # Tentativa de criação testa validade
        except ValueError as e:
            raise ValueError(f"Data inválida: {dia}/{mes}/{ano}") from e

    @property
    def data_sql(self):
        return f"{self.ano:04d}-{self.mes:02d}-{self.dia:02d}"
    
    # Setters com validação automática
    def set_day(self, day):
        self._validar_data(day, self.mes, self.ano)
        self.dia = day
    
    def set_month(self, month):
        self._validar_data(self.dia, month, self.ano)
        self.mes = month
    
    def set_year(self, year):
        self._validar_data(self.dia, self.mes, year)
        self.ano = year
    
    @property
    def data(self):
        return (self.ano, self.mes, self.dia)
    
    @data.setter
    def data(self, valor):
        ano, mes, dia = valor
        self._validar_data(dia, mes, ano)
        self.ano, self.mes, self.dia = ano, mes, dia


x = Data_calendario()
print(x.data_sql)