def cripto_mensagem():
    mensagem = input("Digite a mensagem que deseja criptografar: ")
    with open("mensagem.txt", "w") as arquivo:
        arquivo.write(mensagem)
    print("Mensagem exportada com sucesso!")


if __name__ == "__main__":
    cripto_mensagem() 