import socket
import threading

class HandleHead:
    def get_room_name_size(self, head):
        return int.from_bytes(head[:1],'big')
    
    def get_operation(self, head):
        return int.from_bytes(head[1:2],'big')
    
    def get_state(self, head):
        return int.from_bytes(head[3:4],'big')
    
    def get_operation_payload_size(self, head):
        return int.from_bytes(head[5:],'big')
        
    def get_size(self, head):
        self.room_name_size = self.get_room_name_size(head)
        self.operation_size = self.get_operation(head)
        self.state_size = self.get_state(head)
        self.operation_payload_size = self.get_operation_payload_size(head)

class TCPClient:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address: str = '127.0.0.1'
        self.server_port: int = 55557
    

        self.buffer: int = 32
        self.token_buffer: int = 36
       
        self.client_address: str = ''
        
        self.room_name_size: int = 1
        self.operation: int = 1
        self.state: int = 0
        self.room_name: str =''
        self.host_token: str = ''
        self.user_name: str =''
        self.message: str = ''

    
    def check_appropriate_name_lenght(self,input,num) -> bool:
        lenght: int = len(input)
        return lenght > 0 and lenght <= num
    
    # def check_appropriate_username(self) -> bool:
    #     return self.passwords.find(' ') == -1 and \
    #         len(self.passwords) >= 6 and \
    #         len(self.passwords) <= 11 and \
    #         re.serach('[0-9]', self.passwords) != None and \
    #         re.serach('[A-Z]', self.passwords) != None and \
    #         re.search('[a-z]', self.passwords) != None

    def initialize_chat_room_creation(self) -> None:
        while not self.check_appropriate_name_lenght(self.user_name, 10):
            self.user_name = input('Enter user name(up to 10) -> ')
        print("if you created chat room, enter '1' or jointed chat room, enter '2'")
        self.operation = int(input('Enter 1 or 2 -> '))
        while not self.check_appropriate_name_lenght(self.room_name, 10):
            self.room_name = input('Enter room name(up to 10) -> ')

        
    def initialize_header(self):
        self.room_name_size = 1
        self.operation = 1
        self.state = 0
        self.room_name = ''
        self.host_token = ''
        self.user_name = ''

    # def head_init(self,head: bytes) -> None:
    #     handele_head = HandleHead()
    #     self.room_name_size = handele_head.get_room_name_size(head)
    #     self.operation = handele_head.get_operation(head)
    #     self.status = handele_head.get_state(head)
    #     self.operation_payload_size = handele_head.get_operation_payload_size(head)
    
   
   


    def connect(self):
        while True:
            try:
                self.sock.connect((self.server_address, self.server_port))
                print('Connected to the server {}:{}'.format(self.server_address, self.server_port))
            except Exception as e:
                print('TCPClient occured {}'.format(e))
            
            finally:
                self.chat_start()

    
    def chat_start(self):
        try:
            while True:
                handle_head = HandleHead()

                self.initialize_chat_room_creation()
                self.sock.send(self.buffer)

                
            
                if self.operation == 1:
                    print('create chat room\nstate: {}'.format(self.state))

                    self.state = handle_head.get_state(self.sock.recv(self.buffer))
                    print('state: {}'.format(self.state))

                    self.state = handle_head.get_state(self.sock.recv(self.buffer))
                    print('state: {} n\room created!'.format(self.state))

                    self.client_address = self.sock.recv(self.buffer).decode()

                    break

                elif self.operation == 2:

                    recv_data = self.sock.recv(self.token_buffer).decode()

                    if recv_data == 'TOKEN':
                        message = input('Enter TOKEN -> ')
                        self.sock.send(message).encode()
                        print('chat room created!')
                        self.client_address = self.sock.recv(1).decode()
                        break

        except Exception as e:
            print("YOU CAN'T CONNECT CHAT ROOM")

        finally:
            self.close()

    def close(self):
        print('CLOSE SOCKET')
        self.sock.close()


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
    tcp_client.connect()
    tcp_client.chat_start()

    udp_client = UDP_Client(server_address = '127.0.0.1', client_address='0.0.0.0', user_name = user_name, client_port=8080)
    udp_client.bind_socket()
    udp_client.chat_start()
    # udp_client.closing_socket()

if __name__ == "__main__":
    main()
    