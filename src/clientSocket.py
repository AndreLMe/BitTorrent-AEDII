import socket
from message import Mensagem, deserialize
from baseSocket import BaseSocket

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
        print(mensagem)
        print(mensagem.serialize())
        self.sock.sendall(mensagem.serialize())
        
        
        return self.waitMessage()

        
    def waitMessage(self) -> Mensagem:
        messageBytes = self.sock.recv(1024)
        while len(messageBytes) > 0 and messageBytes[len(messageBytes) - 1] != 0:
            print("in loop")
            messageBytes += self.sock.recv(1024)

        
        if len(messageBytes) == 0:
            print("Mensagem vazia")
            return None
        return deserialize(messageBytes)

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

    def fechar_sock(self):
        pass
        #if self.sock:
        #    self.sock.close()
        #    print(f"Conexão com {self.server} fechada")

