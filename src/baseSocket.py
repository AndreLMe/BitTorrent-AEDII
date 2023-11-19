import message

class BaseSocket:

    def __init__(self, sock):
        self.sock = sock

    def sendAndWaitForResponse(self, message):
        self.sock.sendall(message)
        return self.sock.recv(1024)
    
    def send(self, message: message.Mensagem):
        self.sock.sendall(message.serialize())

    def waitMessage(self):
        return self.sock.recv(1024)