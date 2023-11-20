import threading
from clientSocket import ClientSocket
from message import *
import utils
from datetime import datetime
from piece import Piece
import socket

pieceSize = 2**14 # tamanho de 16384 

class Client:
    
    def __init__(self, host: str, port: int):
        self.menuThread = threading.Thread(target=self.Menu)
        self.clientSocket = ClientSocket(host, port)
        self.menuThread.start()

    def Menu(self):
        while True:
            print("1 - Buscar pedaço")
            print("2 - Verificar pedaço")
            print("3 - Baixar Arquivo")
            print("4 - Baixar pedaço")
            print("5 - Registrar arquivo")
            print("6 - Sair")

            opcao = int(input("Digite a opção desejada: "))
            if opcao == 1:
                self.buscar_pedaco()
            elif opcao == 2:
                self.baixar_arquivo()
            elif opcao == 3:
                self.verificar_pedaco()
            elif opcao == 4:
                self.baixar_pedaco()
            elif opcao == 5:
                self.registrar_arquivo()
            elif opcao == 6:
                break
            else:
                print("Opção inválida!")
    
    def buscar_pedaco(self):
        self.clientSocket.connectAndSend(buscar_pedaco(input("Digite o id do pedaço: ")))

    def registrar_arquivo(self):
        filePath = input("Digite o caminho do arquivo: ")
        #socket = ClientSocket("localhost", 3000)
        fileIdentifier = utils.stringHash((filePath + datetime.now().strftime("%d/%m/%Y %H:%M:%S")).encode())


        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect(("localhost", 3000))
        except socket.error as e:
            print(f"Erro na conexão: {e}")
            s.close()
            s = None
        s.sendall("teste".encode())


        # socket.connect()

        # socket.sock.sendall("test".encode())

        # socket


        # with open(filePath, "rb") as file:
        #     i = 0 
        #     while True:
        #         print("Lendo pedaço")
        #         chunk = file.read(pieceSize)
        #         if not chunk:
        #             break
        #         piece = Piece(fileIdentifier+":"+str(i), chunk)

        #         socket.enviar_mensagem(inserir_pedaco(piece))

                #print("Procurando servidor responsável")
                #r = socket.sendAndWaitForResponse(verificar_pedaco(piece.id, piece.checkSum))
                #while r.messageType == TipoMensagem.BUSCAR_EM_OUTRO_PEER:
                #    print("Tentando em : " + r.payload["peer"][0] + ":" + str(r.payload["peer"][1]))
                #    socket = ClientSocket(r.payload["peer"][0], r.payload["peer"][1])
                #    r = socket.sendAndWaitForResponse(verificar_pedaco(piece.id, piece.checkSum))

                #socket.sendAndWaitForResponse(inserir_pedaco(piece))

                # i += 1

        # filePiecesBytes = utils.splitFile(filePath, pieceSize)

        # print("Arquivo dividido em " + str(len(filePiecesBytes)) + " pedaços")
        # filePieces = []

        # print("Preparando pedaços para envio")
        # for i in range(len(filePiecesBytes)):
        #     filePieces.append(Piece(fileIdentifier+":"+str(i), filePiecesBytes[i]))

        # print("Enviando pedaços")
        # for piece in filePieces:
        #     r = socket.sendAndWaitForResponse(inserir_pedaco(piece))
        #     while r.messageType == TipoMensagem.BUSCAR_EM_OUTRO_PEER:
        #         socket = ClientSocket(r.payload["peer"][0], r.payload["peer"][1])
        #         r = socket.sendAndWaitForResponse(inserir_pedaco(piece))