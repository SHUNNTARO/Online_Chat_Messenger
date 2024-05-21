import socket

class SocketManager:

    def __init__(self,server_adress = None, server_port = 9001):
        if server_adress is None:
            server_adress = Input("Type in the server's address to connect to: ")
        self.server_address = server_adress
        self.server_port = server_port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
