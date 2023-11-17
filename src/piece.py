class Piece:
    def __init__(self) -> None:
        self.id = None
        self.checkSum = None
        self.bytes = []
        self.size = 0
    
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
        #calcular e atribuir o valor do checkSum
    
    @property
    def checkSum(self):
        return self.checkSum