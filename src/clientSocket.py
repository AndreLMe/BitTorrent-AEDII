import socket
from message import Mensagem, deserialize
from baseSocket import BaseSocket
import utils

class ClientSocket:
    def __init__(self: BaseSocket, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = (host, port)
    
    def connect(self):
        try:
            self.sock.connect(self.server)
        except socket.error as e:
            print(f"Erro na conexão: {e}")
            self.sock.close()
            self.sock = None

    def makeRequest(self, mensagem: Mensagem):
        self.connect()
        response = self.sendAndWaitForResponse(mensagem)
        #self.fechar_sock()
        return response
    
    def sendAndWaitForResponse(self, mensagem: Mensagem) -> Mensagem:
        self.connect()
        self.sock.sendall(mensagem.serialize())
        return self.waitMessage()

        
    def waitMessage(self) -> Mensagem:
        return self.waitMessageWithSocket(self.sock)

    def connectAndSend(self, mensagem: Mensagem):
        self.connect()
        self.enviar_mensagem(mensagem)
        self.fechar_sock()

    def enviar_mensagem(self, mensagem: Mensagem):
        if self.sock:
            try:
                self.sock.sendall(mensagem.serialize())
            except socket.error as e:
                print(f"Problemas no envio de {self.server}: {e}")

    def makeRequest(self, address: tuple, mensagem: Mensagem):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(address)
        sock.sendall(mensagem.serialize())

        return self.waitMessageWithSocket(sock)
        
    def waitMessageWithSocket(self, sock: socket.socket) -> Mensagem:
        messageBytes = sock.recv(4096)
        amountOfPackets = utils.parseFromBytes(messageBytes) - 1
        messageBytes = messageBytes[1:]
        while amountOfPackets > 0:
            messageBytes += sock.recv(4096)
            amountOfPackets -= 1

        sock.close()
        return deserialize(messageBytes)


    def fechar_sock(self):
        pass

