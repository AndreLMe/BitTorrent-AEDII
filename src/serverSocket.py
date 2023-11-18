import socket
import threading
import message

class ServerSocket:

    def __init__(self, host, port, onReceiveMessage, socket = None):
        if socket is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.settimeout(5)
        else:
            self.sock = socket
        self.bind(host, port)
        self.onReceiveMessage = onReceiveMessage

    def __init__ (self, socket: socket.socket) -> None:
        self.sock = socket

    def bind(self, host, port):
        self.sock.bind((host, port))

        thread = threading.Thread(target=self.__listen)
        thread.start()

    def waitForConnections(self):
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
            self.onReceiveMessage(parsedMessage, ServerSocket(connectionAndAddress[0]))

    def sendAndWaitForResponse(self, message):
        self.sock.sendall(message)
        return self.sock.recv(1024)
    
    def send(self, message: message.Mensagem):
        self.sock.sendall(message.serialize())

    def waitMessage(self):
        return self.sock.recv(1024)