import socket
import threading
import message
from baseSocket import BaseSocket
import pickle

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
        while True:
            messageBytes = connection.recv(1024)
            while len(messageBytes) > 0 and messageBytes[len(messageBytes) - 1] != 0:
                print("in loop")
                messageBytes += connection.recv(1024)

            
            self.onReceiveMessage(message.deserialize(messageBytes), BaseSocket(connection))

