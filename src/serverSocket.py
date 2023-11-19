import socket
import threading
import message
from baseSocket import BaseSocket

class ServerSocket:
    def __init__(self: BaseSocket, host, port, onReceiveMessage):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.onReceiveMessage = onReceiveMessage
        self.bind(host, port)

    def bind(self, host, port):
        self.sock.bind((host, port))
        self.sock.listen(5)

        thread = threading.Thread(target=self.waitForConnections)
        thread.start()

    def waitForConnections(self):
        print("Esperando por novas conexões")
        while True:
            connectionAndAddress = self.sock.accept()
            thread = threading.Thread(target=self.waitForMessage, args=(connectionAndAddress,))
            thread.start()


    def waitForMessage(self, connectionAndAddress: (socket.socket, tuple)):
        connection = connectionAndAddress[0]
        while True:
            messageBytes = connection.recv(1024)
            while messageBytes[len(messageBytes) - 1] != '\n':
                messageBytes += connection.recv(1024)

            parsedMessage = message.Mensagem(messageBytes)
            self.onReceiveMessage(parsedMessage, BaseSocket(connection))

