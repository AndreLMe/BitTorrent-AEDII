import threading
from clientSocket import ClientSocket
from message import *
import utils
from datetime import datetime
from piece import Piece
import os

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
                self.verificar_pedaco()
            elif opcao == 3:
                self.baixar_arquivo()
            elif opcao == 4:
                self.baixar_pedaco()
            elif opcao == 5:
                self.registrar_arquivo()
            elif opcao == 6:
                break
            else:
                print("Opção inválida!")

    def findServer(self, message: str) -> tuple:
        address = ("localhost", 3000)
        socket = ClientSocket("localhost", 3000)
        r = socket.makeRequest(address, verificar_pedaco(message, ""))
        while r.messageType == TipoMensagem.BUSCAR_EM_OUTRO_PEER:
            socket = ClientSocket("localhost", r.payload["peer"][1])
            r = socket.makeRequest(address, verificar_pedaco(message, ""))
            if r.messageType != TipoMensagem.BUSCAR_EM_OUTRO_PEER:
                break
            address = ("localhost", r.payload["peer"][1])
        return address

    def baixar_arquivo(self):
        socket = ClientSocket("localhost", 3000)
        address = ("localhost", 3000)
        fileIdentifier = input("Digite o id do arquivo: ")
        qtdOfPieces = int(input("Digite a quantidade de pedaços: "))
        fileName = input("Digite o nome do arquivo: ")
        with open(fileName, "wb") as file:
            for i in range(qtdOfPieces):
                print("Baixando pedaço "+str(i))
                idPedaco = fileIdentifier+":"+str(i)
                r = socket.makeRequest(address, buscar_pedaco(idPedaco))
                while r.messageType == TipoMensagem.BUSCAR_EM_OUTRO_PEER:
                    address = ("localhost", r.payload["peer"][1])
                    r = socket.makeRequest(address, buscar_pedaco(idPedaco))
                    if r.messageType != TipoMensagem.BUSCAR_EM_OUTRO_PEER:
                        break
                if r.messageType == TipoMensagem.BUSCAR_PEDACO:
                    print("Pedaço encontrado")
                    print("Baixando...")
                    print(r.payload)
                    file.write(r.payload.bytes)
                else:
                    print("Pedaço não encontrado")
                    break

    def baixar_pedaco(self):
        socket = ClientSocket("localhost", 3000)
        idPedaco = input("Digite o id do pedaço: ")
        print(datetime.now())
        result = socket.makeRequest(self.findServer(idPedaco), buscar_pedaco(idPedaco))
        print(datetime.now())
        if result.messageType == TipoMensagem.BUSCAR_PEDACO:
            print("Pedaço encontrado")
            print("Baixando...")
            print(result.payload)
            with open("pedaco_"+idPedaco, "wb") as file:
                file.write(result.payload.bytes)
        print(datetime.now())
        


    def verificar_pedaco(self):
        socket = ClientSocket("localhost", 3000)
        address = ("localhost", 3000)
        idPedaco = input("Digite o id do pedaço: ")
        
        # Read the file with the name of the piece from disk
        try:
            file = open("pedaco_" + idPedaco, "rb")
            data = file.read()

            # Calculate the checksum
            checksum = utils.stringHash(data)
            r = socket.makeRequest(address, verificar_pedaco(idPedaco, checksum))
            while r.messageType == TipoMensagem.BUSCAR_EM_OUTRO_PEER:
                address = ("localhost", r.payload["peer"][1])
                r = socket.makeRequest(address, verificar_pedaco(idPedaco, checksum))
                if r.messageType != TipoMensagem.BUSCAR_EM_OUTRO_PEER:
                    break

            print(r.payload)
            if r.payload["checkSumIsValid"]:
                print("Pedaço íntegro")

            else:
                print("Pedaço corrompido")

        except Exception as error:
            print("Pedaço não encontrado")
            print(error)
            return


    def buscar_pedaco(self):
        socket = ClientSocket("localhost", 3000)
        socket.makeRequest(buscar_pedaco(input("Digite o id do pedaço: ")))


    def registrar_arquivo(self):
        filePath = input("Digite o caminho do arquivo: ")
        socket = ClientSocket("localhost", 3000)
        fileIdentifier = utils.stringHash((filePath + datetime.now().strftime("%d/%m/%Y %H:%M:%S")).encode())


        address = ("localhost", 3000)
        qtdOfPieces = os.path.getsize(filePath)/pieceSize
        with open(filePath, "rb") as file:
            i = 0 
            while True:
                print("Lendo pedaço")
                print("-->>>>"+str(i)+"/"+str(qtdOfPieces))
                chunk = file.read(pieceSize)
                if not chunk:
                    break
                piece = Piece(fileIdentifier+":"+str(i), chunk)

                print("Procurando servidor responsável")
                r = socket.makeRequest(address, verificar_pedaco(piece.id, piece.checkSum))
                while r.messageType == TipoMensagem.BUSCAR_EM_OUTRO_PEER:
                    socket = ClientSocket("localhost", r.payload["peer"][1])
                    rr = socket.makeRequest(address, verificar_pedaco(piece.id, piece.checkSum))
                    if rr.messageType != TipoMensagem.BUSCAR_EM_OUTRO_PEER:
                        break
                    address = ("localhost", rr.payload["peer"][1])
                    r = rr

                threading.Thread(target=socket.makeRequest, args=(address, inserir_pedaco(piece))).start()

                i += 1


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