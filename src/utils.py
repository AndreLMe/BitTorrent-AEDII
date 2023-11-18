import hashlib

def splitFile( filename: str, pieceSize: int) -> list:
    chunks = []
    with open(filename, "rb") as file:
        while True:
            chunk = file.read(pieceSize)
            if not chunk:
                break
            chunks.append(chunk)
    return chunks

def stringHash(string: str) -> str:
    hash_object = hashlib.sha256(string.encode())
    return hash_object.hexdigest()

def numberHash(string: str) -> int:
    hash_object = hashlib.sha256(string.encode())
    return int(hash_object.hexdigest()[:2], 16)