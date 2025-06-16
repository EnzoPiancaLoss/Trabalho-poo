import datetime
import data_base

import re

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
        print("\n## Dados do Livro:".upper())
        print(f">> Nome: {self.nome}")
        print(f">> Número de páginas: {self.pag}")
        print(f">> ID do Autor: {self.autores}")
        print(f">> ID da Editora: {self.editora}")
        print(f">> Data de Lançamento: {self.lancamento}")

    def Salvar_para_sql(self):
        data_base.Adicionar_dado_a_table_ESPECIFICO(
            "Livro", 
            ["nome", "lancamento", "paginas"], 
            [self.nome, self.lancamento, self.pag]
        )
        resultado = data_base.Ler_dados_da_tabela(
            "Livro", "id_livro", 
            f"nome = '{self.nome}' AND lancamento = '{self.lancamento}'"
        )
        if not resultado:
            print("> Erro: livro não encontrado após inserção.")
            return
        id_livro = resultado[0][0]
        for id_autor in self.autores:
            data_base.Adicionar_dado_a_table_ESPECIFICO(
                "Livro_autor",
                ["id_livro", "id_autor"],
                [id_livro, id_autor]
            )
        if self.editora:
            data_base.Adicionar_dado_a_table_ESPECIFICO(
                "Livro_editora",
                ["id_livro", "id_editora"],
                [id_livro, self.editora]
            )
        print("> Livro e relações inseridos com sucesso.")

class Data_calendario:
    def __init__(self, dia=1, mes=11, ano=2000):
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


class Endereco:
    def __init__(self, CEP: str, Cidade: str, Bairro: str, Rua: str, Estado: str, Numero: str):
        """
        Inicializa um objeto Endereço com validações básicas
        
        Args:
            CEP: String no formato XXXXX-XXX ou XXXXXXXX
            Cidade: Nome da cidade (mínimo 2 caracteres)
            Bairro: Nome do bairro (mínimo 2 caracteres)
            Rua: Nome da rua (mínimo 2 caracteres)
            Estado: Sigla do estado (2 caracteres)
            Numero: Número do endereço (pode conter letras para complementos)
        """
        self.cep = CEP
        self.cidade = Cidade
        self.bairro = Bairro
        self.rua = Rua
        self.estado = Estado
        self.numero = Numero

    @property
    def cep(self) -> str:
        return self._cep
    
    @cep.setter
    def cep(self, value: str):
        value = re.sub(r'[^0-9]', '', value)  # Remove não-numéricos
        if len(value) != 8:
            raise ValueError("CEP deve conter 8 dígitos")
        self._cep = f"{value[:5]}-{value[5:]}"
    
    @property
    def estado(self) -> str:
        return self._estado
    
    @estado.setter
    def estado(self, value: str):
        value = value.upper().strip()
        estados_brasil = {
            'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 
            'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 
            'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'
        }
        if value not in estados_brasil:
            raise ValueError("Estado inválido. Use a sigla de 2 letras")
        self._estado = value
    
    @property
    def cidade(self) -> str:
        return self._cidade
    
    @cidade.setter
    def cidade(self, value: str):
        if not value or len(value.strip()) < 2:
            raise ValueError("Cidade deve ter pelo menos 2 caracteres")
        self._cidade = value.title().strip()
    
    @property
    def bairro(self) -> str:
        return self._bairro
    
    @bairro.setter
    def bairro(self, value: str):
        if not value or len(value.strip()) < 2:
            raise ValueError("Bairro deve ter pelo menos 2 caracteres")
        self._bairro = value.title().strip()
    
    @property
    def rua(self) -> str:
        return self._rua
    
    @rua.setter
    def rua(self, value: str):
        if not value or len(value.strip()) < 2:
            raise ValueError("Rua deve ter pelo menos 2 caracteres")
        self._rua = value.title().strip()
    
    @property
    def numero(self) -> str:
        return self._numero
    
    @numero.setter
    def numero(self, value: str):
        if not value:
            raise ValueError("Número não pode ser vazio")
        self._numero = str(value).strip()
    
    def __str__(self) -> str:
        """Retorna o endereço formatado para correspondência"""
        return f"{self.rua}, {self.numero} - {self.bairro}, {self.cidade}/{self.estado}, {self.cep}"
    
    def to_dict(self) -> dict:
        """Retorna um dicionário com os dados do endereço"""
        return {
            'cep': self.cep,
            'cidade': self.cidade,
            'bairro': self.bairro,
            'rua': self.rua,
            'estado': self.estado,
            'numero': self.numero
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Cria um Endereco a partir de um dicionário"""
        return cls(
            CEP=data.get('cep'),
            Cidade=data.get('cidade'),
            Bairro=data.get('bairro'),
            Rua=data.get('rua'),
            Estado=data.get('estado'),
            Numero=data.get('numero')
        )
    
    def formatado(self) -> str:
        """Retorna o endereço formatado em múltiplas linhas"""
        return (
            f"{self.rua}, {self.numero}\n"
            f"{self.bairro}\n"
            f"{self.cidade}/{self.estado}\n"
            f"CEP: {self.cep}"
        )
    
    def validar(self) -> bool:
        """Valida todos os campos do endereço"""
        try:
            self._validar_cep(self.cep)
            self._validar_estado(self.estado)
            self._validar_cidade(self.cidade)
            self._validar_bairro(self.bairro)
            self._validar_rua(self.rua)
            self._validar_numero(self.numero)
            return True
        except ValueError:
            return False
    
    @staticmethod
    def _validar_cep(cep: str) -> bool:
        cep_limpo = re.sub(r'[^0-9]', '', cep)
        return len(cep_limpo) == 8
    
    @staticmethod
    def _validar_estado(estado: str) -> bool:
        estados = {
            'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 
            'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 
            'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'
        }
        return estado.upper() in estados

x = Data_calendario()
print(x.data_sql)