import socket
import threading
import message
import baseSocket

class ServerSocket:
    def __init__(self: baseSocket.BaseSocket, host, port, onReceiveMessage):
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
            messageBytes = connectionAndAddress[0].recv(1024)
            while messageBytes[len(messageBytes)] != '\n':
                messageBytes += connectionAndAddress[0].recv(1024)

            parsedMessage = message.Mensagem(messageBytes)
            self.onReceiveMessage(parsedMessage, baseSocket.BaseSocket(connectionAndAddress[0]))

