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
        self.sock.connect((self.server_address, self.server_port))

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

        self.sock.sendall(header + body)

        response = self.sock.recv(self.buffer + 255)
        response_state = response[1]
        token_size = response[3]
        token = response[4:4 + token_size].decode()

        print('f"Recieved token: {token}')



    def start(self):
        self.connect()
        self.create_chat_room()
        threading.Thread(target=self.recv_data).start()
        threading.Thread(target=self.write).start()

if __name__ == "__main__":
    tcp_client = TCPClient()
    tcp_client.user_name = input('Enter your name -> ')
    tcp_client.room_name = input('Enter the room name -> ')
    tcp_client.start()
                
                
