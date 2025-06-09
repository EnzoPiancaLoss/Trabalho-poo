def exibir_cli(escolhas_disponiveis, saida_nome="Voltar"):
    if "0" in escolhas_disponiveis:
        print("Por favor não incluir 0 no dicionário para as escolhas disponíveis")
        return
    else:
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
