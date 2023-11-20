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

def stringHash(bytes: bytes) -> str:
    hash_object = hashlib.sha256(bytes)
    return hash_object.hexdigest()

def numberHash(bytes: bytes) -> int:
    hash_object = hashlib.sha256(bytes)
    return int(hash_object.hexdigest()[:2], 16)