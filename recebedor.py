def importar_mensagem():
    try:
        with open("mensagem.txt", "r") as arquivo:
            mensagem = arquivo.read()
        print(f"Mensagem importada: {mensagem}")
    except FileNotFoundError:
        print("O arquivo 'mensagem.txt' não foi encontrado!")


if __name__ == "__main__":
    importar_mensagem()