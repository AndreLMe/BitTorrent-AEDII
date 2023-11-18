from enum import Enum
import json

class TipoMensagem(Enum):
    BUSCAR_PEDACO = 1
    INSERIR_PEDACO = 2
    VERIFICAR_PEDACO = 3
    BUSCAR_EM_OUTRO_PEER = 4

class Mensagem:
    def __init__(self, message: bytes) -> None:
        self.messageType, self.payload = self.deserialize(message)

    def __init__(self, messageType : TipoMensagem, payload: bytes) -> None:
        self.payload = payload
        self.messageType = messageType

    def serialize(self) -> bytes:
        return (json.dumps(self.__dict__)+"\n").encode()

    def deserialize(self, message: bytes) -> None:
        return json.loads(message.decode())
