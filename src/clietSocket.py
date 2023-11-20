import socket
from message import Mensagem
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

    def enviar_mensagem(self, mensagem: Mensagem):
        if self.sock:
            try:
                self.sock.sendall(mensagem.serialize)
            except:
                print(f"Problemas no envio de {self.server}")

    def fechar_sock(self):
        if self.sock:
            self.sock.close()
            print(f"Conexão com {self.server} fechada")
