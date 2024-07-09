import socket
import threading
import struct
import json

class TCPServer:
    def __init__(self):
        self.server_address: str = '127.0.0.1'
        self.server_port: int = 55557
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.buffer:int = 32

        self.room_name_size: int = 1
        self.operation: int = 1
        self.state: int = 1
        self.operation_payload_size:int = 29


        self.clients = {}
        self.chat_rooms = {}

    def sock_bind(self) -> None:
        self.sock.bind((self.server_address, self.server_port))
        print('TCP SERVER start up on {}, port {}'.format(self.server_address, self.server_port))
        self.sock.listen(5)
    
    def handle_client(self, connection, client_address):
        try:
            while True:
                header = connection.recv(self.buffer)
                if not header:
                    break

                room_name = connection.recv(self.room_name_size).decode()
                operation_payload= connection.recv(self.operation_payload_size).decode()

                if self.operation == 1: # create chat room
                    self.handle_create_chat_room(connection, room_name, self.state, operation_payload, self.room_name_size, self.operation, client_address)
                elif self.operation == 2: # join chat room
                    self.handle_join_chat_room(connection, room_name, self.state, operation_payload, self.room_name_size, self.operation, client_address)
        except struct as err:
            print('Occured error about struct, {}'.format(err))
        except socket.error as err:
            print('Occured error about socket, {}'.format(err))
        except Exception as err:
            print('Occured error, {}'.format(err))
        finally:
            connection.close()

    def handle_create_chat_room(self, connection, room_name, state, operation_payload, client_address):
        if state == 0:
            user_name = operation_payload
            token = self.handle_create_chat_room(room_name, user_name, client_address)
            response_payload = json.dump({'status': 'success', 'token': token})
            self.send_response(connection, self.room_name_size, self.operation, 2, response_payload)
        elif state == 1:
            pass
        elif state == 2:
            pass
    
    def send_response(self, connection, state, response_payload):
        header = connection.recv(self.buffer) 
        response_payload_length: int = len(response_payload)

        room_name_size_length: bytes = self.room_name_size.to_bytes(1, byteorder='big')
        operation_length: bytes = self.operation.to_bytes(1, byteorder='big')
        state_length: bytes = state.to_bytes(1, byteorder='big')
        operation_payload_size_length: bytes = self.operation_payload_size.to_bytes(29, byteorder='big')

        response_header = room_name_size_length + operation_length + state_length + operation_payload_size_length
        connection.sendall(response_header + response_payload.encode())



    def create_chat_room(self, room_name, user_name, client_address):
        token = f'{room_name}_{user_name}'
        self.chat_rooms[room_name] = {'host': token, 'client': {token: client_address}}
        return token
    
    def join_chat_room(self, room_name, user_name, client_address):
        token = f'{room_name}_{user_name}_{client_address[0]}'
        if room_name in self.chat_rooms:
            self.chat_rooms[room_name]['client'][token] = client_address
        return token
    
    def recv_data(self):
        while True:
            connection, client_addres = self.sock.accept()
            print('Connected with {}'.format(client_addres))
            thread = threading.Thread(target=self.handle_client, args=(connection, client_addres))
            thread.start()

    def close_sock(self):
        print("TCP SERVER closing...")
        self.sock.close()

def main():
    tcp_server = TCPServer()
    tcp_server.sock_bind()
    thread_tcp = threading.Thread(target=tcp_server.recv_data)
    thread_tcp.start()
    thread_tcp.join()

if __name__ == "__main__":
    main()

