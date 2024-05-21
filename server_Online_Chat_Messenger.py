import socket


class SocketManager:
    def __init__(self, server_address = '0.0.0.0', server_port = 9001):
        self.server_address = server_address
        self.server_port = server_port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    def socket_bind(self):
        self.sock.bind((self.server_address,self.server_port))

class Data_Handler:
    def __init__(self,sock):
        self.sock = sock

    def recieve_data(self):
        data, address = self.sock.recvfrom(4096)
        print('received {} bytes from {}'.format(len(data), address))
        print(data)
        return data, address

    def send_data(self,data,address):
        sent = self.sock.sendto(data, address)
        print('sent {} bytes back to {}'.format(sent,address))


if __name__ == "__main__":

    sock_manager = SocketManager()

    sock_manager.socket_bind()

    data_handler = Data_Handler(sock_manager.sock)

    while True:
        data,address = data_handler.recieve_data()
        data_handler.send_data(b'ACK', address)