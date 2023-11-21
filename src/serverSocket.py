import socket
import threading
import message
from baseSocket import BaseSocket
import pickle
import utils

class ServerSocket:
    def __init__(self, host, port, onReceiveMessage):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.onReceiveMessage = onReceiveMessage
        self.host = host
        self.port = port

    def start(self):
        self.bind(self.host, self.port)
        self.waitForConnections()

    def bind(self, host, port):
        self.sock.bind((host, port))
        self.sock.listen(5)

    def waitForConnections(self):
        print("Esperando conexões")
        while True:
            print("Esperando conexões dentro do while")
            connectionAndAddress = self.sock.accept()
            print("Conexão recebida")
            thread = threading.Thread(target=self.waitForMessages, args=(connectionAndAddress,))
            thread.start()

    def waitForMessages(self, connectionAndAddress: (socket.socket, tuple)):
        print("Nova conexão recebida")
        connection = connectionAndAddress[0]
        try:
            while True:
                messageBytes = connection.recv(4096)
                if not messageBytes:
                    break
                amountOfPackets = utils.parseFromBytes(messageBytes) - 1
                print(amountOfPackets)
                messageBytes = messageBytes[1:]
                while amountOfPackets > 0:
                    print("in loop")
                    messageBytes += connection.recv(4096)
                    amountOfPackets -= 1

                self.onReceiveMessage(message.deserialize(messageBytes), BaseSocket(connection))
        except Exception as e:
            print(e.with_traceback())
            print("Conexão encerrada")
            connection.close()
            return
