from serverSocket import ServerSocket
from baseSocket import BaseSocket
from message import Mensagem, TipoMensagem
from piece import Piece

class Tracker:
    def __init__(self) -> None:
        self.socket = ServerSocket("localhost", 2003)
        self.list_peers = [("peer-"+ str(i+1), 3000 + i) for i in range(0,5)]
        self.lista_de_retorno = []
    
    def iniciar_listen(self, message:Mensagem, connection: BaseSocket):
        
        if message.messageType == TipoMensagem.VERIFICAR_PEDACO:
            connection.sendAndWaitForResponse(Mensagem(
                TipoMensagem.VERIFICAR_PEDACO, 
                Piece(message.payload)))

    def buscar_pedacos(self):
        pass

    def enviarRespostaParaCliente(self):
        pass