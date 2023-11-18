import utils

class Piece:
    def __init__(self) -> None:
        self.id = None
        self.checkSum = None
        #Ta fazendo os arquivos sempre ficarem alocados in memory talvez mudar isso pra pegar da mem sec
        self.bytes = []
        self.size = 0

    def __init__(self, id: str, bytes: bytes) -> None:
        self.id = id
        self.bytes = bytes
        self.size = len(bytes)
        self.checkSum = utils.stringHash(bytes)
    
    @property
    def id(self):
        return self.id
    
    @id.setter
    def id(self, valor):
        self.id = valor
    
    @property
    def bytes(self):
        return self.bytes
    
    @bytes.setter
    def bytes(self, bytes):
        self.bytes = bytes
    
    @property
    def checkSum(self):
        return self.checkSum