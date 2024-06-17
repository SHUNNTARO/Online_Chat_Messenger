import socket
import threading

class TCPClient:
    def __init__(self):
        self.server_address: str = '127.0.0.1'
        self.server_port: int = 55557
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.message: str = ""
        self.user_name: str =""
        self.room_name: str =""

        self.buffer: int = 32
        self.state: int = 1
        self.operation: int = 1


    def connect(self):
        print(f'Connecting to {self.server_address}:{self.server_port}')
        self.sock.connect((self.server_address, self.server_port))
        print('Connected to the server')

    def create_chat_room(self):
        room_name_size: int = len(self.room_name.encode())
        operation_payload_size: int = len(self.user_name.encode())
        state = 0
        operation = 1

        room_name_size_byte: bytes = room_name_size.to_bytes(1, byteorder='big')
        operation_payload_size_bytes: bytes = operation_payload_size.to_bytes(1, byteorder='big')
        state_bytes: bytes = state.to_bytes(1, byteorder='big')
        operation_bytes: bytes = operation.to_bytes(1, byteorder='big')

        header = room_name_size_byte + operation_bytes +state_bytes + operation_payload_size_bytes 
        body = self.room_name.encode() + self.user_name.encode()

        print(f'Sending chat room creation request: room_name={self.room_name}, user_name={self.user_name}')
        self.sock.sendall(header + body)

        response = self.sock.recv(self.buffer + 255)
        response_state = response[2]
        token_size = response[3]
        token = response[4:4 + token_size].decode()

        if response_state == 2:
            print('f"Recieved token: {token}')
        else:
            print("Failed to create chat room")

    def join_chat_room(self, room_name, token):
        room_name = self.room_name

        state: int = 0
        operation: int = 2
        room_name_size:int = len(room_name)
        operation_payload = token
        operation_payload_size: int = len(operation_payload)

        state_bytes: bytes = state.to_bytes(1, byteorder='big')
        operation_bytes: bytes = operation.to_bytes(1, byteorder='big')
        room_name_bytes: bytes = room_name_size.to_bytes(1, byteorder='big')
        operation_payload_bytes: bytes = operation_payload_size.to_bytes(1, byteorder='big')

        header = state_bytes + operation_bytes + room_name_bytes + operation_payload_bytes
        self.sock.sendall(header + room_name.encode() + operation_payload.encode())

        response = self.sock.recv(self.buffer).decode()
        response_data = json.loads(response)
        if response_data['status'] == 'success':
            print(f"jointed chat room '{room_name}' successfully as {response_data['user_name']}")
        else:
            print(f"Failed to join chat room '{room_name}': {response_data['reason']}")

    def sent_data(self):
        while True:
            try:
                self.message = input("")
                self.sock.sendall(self.message.encode())
            except Exception as e:
                print('An error occured: {}'.format(e))
            self.sock.settimeout(2)

    
    def recv_data(self):
        while True:
            try:
                recv_data = self.sock.recv(self.buffer).decode()
                if recv_data == 'NICK':
                    self.sock.sendall(self.user_name.encode())
                else:
                    print(recv_data)
            except Exception as e:
                print('An error occured {}'.format(e))

    def write(self):
        while True:
            self.message = '{}: {}'.format(self.user_name, input(''))
            self.sock.sendall(self.message.encode())


    def start(self):
        self.connect()
        self.create_chat_room()
        threading.Thread(target=self.recv_data).start()
        threading.Thread(target=self.write).start()


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
        print(f'Binding socket to {self.client_address}:{self.client_port}')
        self.sock.bind((self.client_address, self.client_port))
        print('Socket bound')

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
            self.sock.sendto(send_data,(self.server_address, self.server_port))
            

    def recv_message(self) -> None:
        while True:
            try:
                recv_data, _ = self.sock.recvfrom(self.bytes)
                user_name_length = recv_data[0]
                user_name = recv_data[1:user_name_length+1].decode()
                recv_message = recv_data[user_name_length+1:].decode()
                print('{}: {}'.format(user_name, recv_message))
            except Exception as e:
                print('An error occured: {}'.format(e))


    def closing_socket(self) -> None:
        print('closing socket')
        self.sock.close()       

    def chat_start(self):
        recv_thread = threading.Thread(target=self.recv_message)
        recv_thread.daemon = True
        recv_thread.start()
        self.send_message()


def main():
    user_name = input('Enter your name... ')
    room_name = input('Enter the room name... ')
    
    tcp_client = TCPClient()
    tcp_client.user_name = user_name
    tcp_client.room_name = room_name
    tcp_client.start()

    udp_client = UDP_Client(server_address = '127.0.0.1', client_address='0.0.0.0', user_name = user_name, client_port=8080)
    udp_client.bind_socket()
    udp_client.chat_start()
    udp_client.closing_socket()

if __name__ == "__main__":
    main()
    