from message import Mensagem, TipoMensagem


def main():
    print("Carregando demonstração...")
    while True:
        input()

if __name__ == '__main__':
    try:
        print("Iniciando...")
        main()
    except KeyboardInterrupt:
        print("Exiting...")