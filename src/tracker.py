import socket
import message
import piece

class Tracker:
    def __init__(self) -> None:
        self.port = 1099
        self.ip = "localhost"
        self.list_peers = []
    
    def iniciar_listen(self):
        with socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.ip, self.port))
            s.listen()
    
    def buscar_pedacos(self):
        pass

    def enviarRespostaParaCliente(self):
        pass