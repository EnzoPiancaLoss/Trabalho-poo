from cli import exibir_cli

main_menu = {
    "1": "Cadastrar livro",
    "2": "Exibir livros",
    "3": "Relatório de empréstimo"
}

# O parâmetro deve ser um dicionário
# Nunca pode conter a chave "0", pois ela está reservada para o botão de sair

exibir_cli(main_menu)
