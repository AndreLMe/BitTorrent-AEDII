from piece import Piece
from serverSocket import ServerSocket
from baseSocket import BaseSocket
from message import Mensagem, TipoMensagem
import json
import utils
from serverInfo import ServerInfo


pieceSize = 2**14 # tamanho de 16384 

class Peer:
    def __init__(self, addr: tuple, knownPeers: list[ServerInfo], maxIdHash: int, 
                 sucessor: ServerInfo, predecessor: ServerInfo ):
        print("Iniciando peer")
        
        self.addr = addr
        self.id = None
        self.selfPieces = {}
        self.sucessor = sucessor
        self.predecessor = predecessor
        self.knownPeers = knownPeers # {"addr": (ip, port), "maxIdHash": 0}
        self.maxIdHash = maxIdHash
        self.socket = ServerSocket(addr[0], addr[1], self.__listen)
        self.socket.start()
    
    def __listen(self, message: Mensagem, connection: BaseSocket):
        print("Mensagem recebida")
        print(message.messageType)
        if message.messageType == TipoMensagem.BUSCAR_PEDACO:
            if self.amITheResponsible(utils.numberHash(message.payload.encode())):
                print("Sou responsável por esse pedaço: " + message.payload)
                piece = self.searchPiece(message.payload)
                connection.send(Mensagem(TipoMensagem.BUSCAR_PEDACO, piece))

            else:
                print("Não sou responsável por esse pedaço: " + message.payload)
                connection.send(Mensagem(TipoMensagem.BUSCAR_EM_OUTRO_PEER, {
                    "peer": self.searchNearPeer(message.payload).addr,
                }))

        elif message.messageType == TipoMensagem.VERIFICAR_PEDACO:
            pieceIdHash = utils.numberHash(message.payload["id"].encode())
            if not self.amITheResponsible(pieceIdHash):
                connection.send(Mensagem(TipoMensagem.BUSCAR_EM_OUTRO_PEER, {
                    "peer": self.searchNearPeer(message.payload["id"]).addr,
                }))
                return
            
            print("Sou responsável por esse pedaço: " + str(pieceIdHash))

            localPiece = self.searchPiece(message.payload["id"])

            checkSumIsValid = localPiece is not None and message.payload["checkSum"] == localPiece.checkSum

            response = {"checkSumIsValid":checkSumIsValid}

            connection.send(Mensagem(TipoMensagem.VERIFICAR_PEDACO, response))

        elif message.messageType == TipoMensagem.INSERIR_PEDACO:
            pieceIdHash = utils.numberHash(message.payload.id.encode())
            if self.amITheResponsible(pieceIdHash):
                self.selfPieces[message.payload.id] = message.payload
                print("Pedaço inserido com sucesso: "+message.payload.id)
                connection.send(Mensagem(TipoMensagem.INSERIR_PEDACO, "OK"))
            else:
                connection.send(Mensagem(TipoMensagem.BUSCAR_EM_OUTRO_PEER, {
                    "peer": self.searchNearPeer(message.payload.id).addr,
                }))
        else:
            pass

    def amITheResponsible(self, pieceIdHash: int) -> bool:
        print("Comparando " + str(pieceIdHash) + " com " + str(self.maxIdHash))
        print(pieceIdHash <= self.maxIdHash)
        print(pieceIdHash > self.predecessor.maxIdHash)


        predIsLast = self.predecessor.maxIdHash >= 255
        
        if predIsLast:
            return pieceIdHash <= self.maxIdHash

        return pieceIdHash <= self.maxIdHash and pieceIdHash > self.predecessor.maxIdHash
    
    def isNearPeer(self, pieceHash: str, previous: str, now: str) -> bool:
        return pieceHash <= now and pieceHash > previous

    def searchPiece(self, pieceId: str) -> Piece:
        return self.selfPieces.get(pieceId)

    def searchNearPeer(self, pieceId: str) -> ServerInfo:
        toReturnPeer = None
        pieceIdHash = utils.numberHash(pieceId.encode())

        if self.sucessor.maxIdHash >= pieceIdHash and pieceIdHash > self.maxIdHash:
            print("Retornando para tentar em(): " + str(self.sucessor.addr))
            return self.sucessor

        # Will iterate over the known peers and return the one with the highest id hash that is smaller than the piece id hash
        for i in range(1,len(self.knownPeers)):
            peer = self.knownPeers[i]

            if self.isNearPeer(pieceIdHash, self.knownPeers[i-1].maxIdHash, peer.maxIdHash):
                toReturnPeer = self.knownPeers[i-1]
                break
        else:
            toReturnPeer = self.knownPeers[len(self.knownPeers)-1]

        print("Retornando para tentar em: " + str(toReturnPeer.addr))
        return toReturnPeer

    def registerFile(self, filename: str, uniqueIdentifier: str) -> dict:
        splitedFile = utils.splitFile(filename, pieceSize)
        for i in range(len(splitedFile)):
            piece = Piece(uniqueIdentifier + str(i), splitedFile[i])
            self.selfPieces[piece.id] = piece