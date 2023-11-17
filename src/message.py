from enum import Enum

class TipoMensagem(Enum):
    BUSCAR_PEDACO = 1
    INSERIR_PEDACO = 2
    VERIFICAR_PEDACO = 3

class Message:
    def __init__(self) -> None:
        pass