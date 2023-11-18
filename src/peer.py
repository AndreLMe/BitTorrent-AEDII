import piece as pieceObj
import serverSocket
import message as messagePackage
import json
import utils

pieceSize = 2**14 # tamanho de 16384 

class Peer:
    def __init__(self, addr: tuple) -> None:
        self.addr = addr
        self.id = None
        self.socket = serverSocket.ServerSocket(addr[0], addr[1], self.__listen)
        self.pieces = {}
        self.sucessor = None
        self.predecessor = None
        self.knownPeers = [] # {"addr": (ip, port), "maxIdHash": 0}
        self.maxIdHash = None
    
    def __listen(self, message: messagePackage.Mensagem, connection: serverSocket.ServerSocket):
        if message.messageType == messagePackage.TipoMensagem.BUSCAR_PEDACO:
            connection.send(messagePackage.Mensagem(messagePackage.TipoMensagem.BUSCAR_PEDACO, self.searchPiece(message.payload)))

        elif message.messageType == messagePackage.TipoMensagem.INSERIR_PEDACO:
            pass
        elif message.messageType == messagePackage.TipoMensagem.VERIFICAR_PEDACO:
            pieceIdHash = utils.numberHash(message["payload"]["id"])
            if pieceIdHash > self.maxIdHash or self.predessor.maxIdHash > pieceIdHash:
                connection.send(messagePackage.Mensagem(messagePackage.TipoMensagem.BUSCAR_EM_OUTRO_PEER, {
                    "peer": self.searchProbablePeer(message["payload"]["id"])["addr"],
                }))
            
            checkSumIsValid = message["payload"]["checkSum"] == self.searchPiece(message["payload"]["id"]).checkSum

            response = {"checkSumIsValid":checkSumIsValid}

            responsePayload = json.dumps(response).encode()

            connection.send(messagePackage.Mensagem(messagePackage.TipoMensagem.VERIFICAR_PEDACO, responsePayload))
        else:
            pass
        
    def searchPiece(self, pieceId: str) -> pieceObj.Piece:
        return self.pieces[pieceId]


    def searchProbablePeer(self, pieceId: str) -> tuple:
        toReturnPeer = None

        # Will iterate over the known peers and return the one with the highest id hash that is smaller than the piece id hash
        for peer in self.knownPeers:
            if utils.numberHash(pieceId) < utils.numberHash(peer["maxIdHash"]):
                break
            toReturnPeer = peer

        return toReturnPeer

    def registerFile( filename: str, uniqueIdentifier: str) -> dict:
        splitedFile = utils.splitFile(filename, pieceSize)
        for i in range(len(splitedFile)):
            piece = pieceObj.Piece(uniqueIdentifier + str(i), splitedFile[i])
            self.pieces[piece.id] = piece



