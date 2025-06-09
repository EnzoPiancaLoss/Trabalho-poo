import classes as cla
import data_base as db
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

def cadastrar_livros_cli():
    print("Cadastrar livros")

    nome_livro = str(input("Nome do livro "))
    
    print("Inserir autores")

    r = 1
    q = 0
    a = []
    while r > 0:
        r = int(input(f"Inserir 0 vai parar de adicionar\nAutor id {q + 1}: "))
        if a == [] and r == 0:
            print("> Coloque pelo menos 1 autor")
            r = 1
        elif r == 0 and len(a) >= 1:
            break
        else:
            if db.Existe_dado_na_tabela("Autor", f"id_autor = {r}"):
                resultado = db.Ler_dados_da_tabela("Autor", "nome_autor", f"id_autor = {r}")
                nome_autor = resultado[0][0] if resultado else "Desconhecido"
                print(f"Autor adicionado: {nome_autor}\n")
                a.append(r)
                q += 1
                print("Array: ", a)
            else:
                print("Autor não encontrado. Tente outro ID.\n")
    

    print("Inserir editora")
    print("O Livro tem uma editora? (S/N)")
    tem_editora = -1
    while tem_editora == -1:
        resposta = input("Tem editora? (S/N): ").strip().upper()

        if resposta == "S":
            tem_editora = 1
        elif resposta == "N":
            tem_editora = 0
            print("> Sem editora")
        else:
            print("> Responda apenas com S ou N.")

    editora_id = None
    if tem_editora == 1:
        while True:
            editora_id = int(input("Id da editora: "))
            if db.Existe_dado_na_tabela("Editora", f"id_editora = {editora_id}"):
                resultado = db.Ler_dados_da_tabela("Editora", "nome_editora", f"id_editora = {editora_id}")
                nome_2 = resultado[0][0] if resultado else "Desconhecida"
                print(f"> Editora selecionada: {nome_2}\n")
                print("> Id: ", editora_id)
                break
            else:
                print("> Editora não encontrada. Tente outro ID.\n")



    paginas = str(input("Quantidade de paginas "))
    x = cla.Data_calendario()

    print("Data de publicação ")
    x.set_year(int(input("Ano "))) 
    x.set_month(int(input("Mes ")))
    x.set_day(int(input("Dia ")))

    print("Data:", x.data_sql)


    y = cla.Insercao_livro(nome_livro,paginas,a,editora_id,x.data_sql)
    return y
    pass