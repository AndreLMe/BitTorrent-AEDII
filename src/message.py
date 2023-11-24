from enum import Enum
import json
from piece import Piece
import pickle
import math

class TipoMensagem(Enum):
    BUSCAR_PEDACO = 1
    INSERIR_PEDACO = 2
    VERIFICAR_PEDACO = 3
    NOVO_PEER = 4
    PROXIMO_PEER = 5
    ANTERIOR_PEER = 6
    BUSCAR_EM_OUTRO_PEER = 7

class Mensagem:
    def __init__(self, messageType: TipoMensagem = None, payload = None):
        self.payload = payload
        self.messageType = messageType
    
    def serialize(self) -> bytes:
        pickleBytes = pickle.dumps(self)
        amountOfPackages = math.ceil((len(pickleBytes)+1) / 4096)
        intBytes = amountOfPackages.to_bytes(1,signed=False)
        return intBytes + pickleBytes

    def jsonSerialize(self) -> bytes:
        return json.dumps({"messageType": self.messageType.value, "payload": self.payload}).encode()
    
def deserialize(messageBytes: bytes) -> Mensagem:
    return pickle.loads(messageBytes)

def buscar_pedaco(pieceId: str):
    return Mensagem(TipoMensagem.BUSCAR_PEDACO, pieceId)

def inserir_pedaco(piece: Piece):
    return Mensagem(TipoMensagem.INSERIR_PEDACO, piece)

def verificar_pedaco(id: Piece, checkSum: str):
    return Mensagem(TipoMensagem.VERIFICAR_PEDACO, {"id": id, "checkSum": checkSum})