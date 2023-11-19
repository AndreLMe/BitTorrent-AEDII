from enum import Enum
import json
from piece import Piece
import pickle

class TipoMensagem(Enum):
    BUSCAR_PEDACO = 1
    INSERIR_PEDACO = 2
    VERIFICAR_PEDACO = 3
    NOVO_PEER = 4
    PROXIMO_PEER = 5
    ANTERIOR_PEER = 6

class Mensagem:
    def __init__(self, message: bytes, sender: (str, int)) -> None:
        self.messageType, self.payload = self.deserialize(message)
        self.sender = sender

    def __init__(self, messageType : TipoMensagem, payload: bytes, sender: (str, int)) -> None:
        self.payload = payload
        self.messageType = messageType
        self.sender = sender

    def __init__(self, messageType : TipoMensagem, sender: (str, int)) -> None:
        self.messageType = messageType
        self.sender = sender
    
    def serialize(self) -> bytes:
        return (json.dumps(self.__dict__)+"\n").encode()

    def deserialize(self, message: bytes) -> None:
        return json.loads(message.decode())


def novo_node(addr: (str, int)):
    return Mensagem(TipoMensagem.NOVO_PEER, addr)

def buscar_pedaco(addr: (str, int), piece: Piece):
    return Mensagem(TipoMensagem.BUSCAR_PEDACO, pickle.dumps(piece), addr)

def inserir_pedaco(addr: (str, int), piece: Piece):
    return Mensagem(TipoMensagem.INSERIR_PEDACO, pickle.dumps(piece), addr)

def verificar_pedaco(addr: (str, int), piece: Piece):
    return Mensagem(TipoMensagem.VERIFICAR_PEDACO, pickle.dumps(piece), addr)