import socket
import threading

class UDP_Client:
    def __init__(self,server_address: str, client_address: str, user_name: str, client_port: int = 8080) -> None:
        self.server_address = server_address
        self.server_port: int = 55557
        self.client_port: int = client_port
        self.client_address:str = client_address
        self.bytes: int = 4096
        self.user_name = user_name

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


    def bind_socket(self) -> None:
        self.sock.bind((self.client_address, self.client_port))

    def send_message(self) -> None:
        print('Enter your message or if you would quite a chat, enter "exit"')
        while True:
            message: str = input('')
            if message.lower() == 'exit':
                break
            user_name_bytes: bytes = self.user_name.encode()
            message_bytes: bytes = message.encode()
            user_name_length:int = len(user_name_bytes)
            send_data = bytes([user_name_length]) + user_name_bytes + message_bytes
            send_data_str: str = send_data.decode()
            self.sock.sendto(send_data,(self.server_address, self.server_port))
            

    def recv_message(self) -> None:
        while True:
            recv_data, _ = self.sock.recvfrom(self.bytes)
            user_name_length = recv_data[0]
            user_name = recv_data[1:user_name_length+1].decode()
            recv_message = recv_data[user_name_length+1:].decode()
            print('{}: {}'.format(user_name, recv_message))

    def closing_socket(self) -> None:
        print('closing socket')
        self.sock.close()       

    def chat_start(self):
        threading.Thread(target=self.recv_message).start()
        self.send_message()
        

if __name__ == "__main__":
    user_name = input('Enter your name... ')
    server_address = '127.0.0.1'
    client = UDP_Client(server_address = server_address, client_address='0.0.0.0', user_name = user_name, client_port=8080)
    client.bind_socket()
    client.chat_start()
    client.closing_socket()