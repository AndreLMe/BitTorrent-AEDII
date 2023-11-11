class Peer:
    def __init__(self, addr: tuple) -> None:
        self.addr = addr
        self.id = None
        self.pieces = []
        _list()
    
    def __listen(self):
        pass