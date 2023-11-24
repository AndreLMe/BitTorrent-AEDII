import utils

class Piece:
    def __init__(self, id: str, bytes: bytes) -> None:
        self.id = id
        self.bytes = bytes
        self.size = len(bytes)
        self.checkSum = utils.stringHash(bytes)