import socket

class UDP_Client:
    def __init__(self,server_adress = None, server_port = 9001, client_port = 9050, client_address:str = '127.0.0.1') -> None:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        if server_adress is None:
            server_adress = input("Type in the server's address to connect to: ")
        self.server_address = server_adress
        self.server_port = server_port
        self.client_address = client_address
        self.client_port = client_port

        
    def bind_socket(self)-> None:
        self.sock.bind((self.client_address, self.client_port))
 
    def handle_message(self,message)->None:
        self.message = message
        try:
            print('sending {!r}'.format(self.message))
            sent = self.sock.sendto(self.message.encode(), (self.server_address, self.server_port))
            print('Send {} bytes'. format(sent))

            print('waiting to receive')
            data,server = self.sock.recvfrom(4096)
            print('recived {!r}'.format(data.decode()))
        except Exception:
            print('An error occurred: {}'.format(Exception))
 
    def closing_socket(self)->None:
        print('closing socket')
        self.sock.close()

if __name__ == "__main__":
    client = UDP_Client(server_adress='127.0.0.1', server_port=9001, client_port=9050)
    client.bind_socket()
    client.handle_message("Hellp, Server!")
    client.closing_socket()