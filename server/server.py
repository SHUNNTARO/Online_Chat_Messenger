import socket
import threading
import struct
import json
import time

class Client_info:
    def __init__(self, user_name, client_address):
        self.user_name = user_name
        self.client_address = client_address
        self.last_response = time.time()


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
            token = self.create_chat_room(room_name, user_name, client_address)
            response_payload = json.dump({'status': 'success', 'token': token})
            self.send_response(connection, 2, response_payload)
        elif state == 1:
            pass
        elif state == 2:
            pass

    def handle_join_chat_room(self, connection, room_name, state, operation_payload, client_address):
        if state == 0:
            token = operation_payload
            if room_name in self.chat_rooms and self.chat_rooms[room_name]['host'] == token:
                user_name = f"User_{len(self.chat_rooms[room_name]['client'] + 1)}"
                self.chat_rooms[room_name]['cient'][token] = client_address
                response_payload = json.dump({'status': 'failure', 'reason': 'Invalid room or token'})
                self.send_response(connection, 2, response_payload)
            elif state == 1:
                pass
            elif state == 2:
                pass
    
    def send_response(self, connection, state, response_payload):
        response_payload_length: int = len(response_payload)

        room_name_size_bytes: bytes = self.room_name_size.to_bytes(1, byteorder='big')
        operation_bytes: bytes = self.operation.to_bytes(1, byteorder='big')
        state_bytes: bytes = state.to_bytes(1, byteorder='big')
        operation_payload_size_bytes: bytes = response_payload_length.to_bytes(29, byteorder='big')

        response_header = room_name_size_bytes + operation_bytes + state_bytes + operation_payload_size_bytes
        connection.sendall(response_header + response_payload.encode())


    def create_chat_room(self, room_name, user_name, client_address):
        token = f'{room_name}_{user_name}'
        self.chat_rooms[room_name] = {'host': token, 'client': {token: client_address}}
        print(f'Chat room created: {self.chat_rooms[room_name]}')
        return token
    
    def join_chat_room(self, room_name, user_name, client_address):
        token = f'{room_name}_{user_name}_{client_address[0]}'
        if room_name in self.chat_rooms:
            self.chat_rooms[room_name]['client'][token] = client_address
        print(f'Client joined chat room: {self.chat_rooms[room_name]}')
        return token
    
    def start(self):
        self.sock_bind()
        while True:
            connection, client_addres = self.sock.accept()
            print('Connected with {}'.format(client_addres))
            thread = threading.Thread(target=self.handle_client, args=(connection, client_addres))
            thread.start()

    def close_sock(self):
        print("TCP SERVER closing...")
        self.sock.close()



class UDP_Server:
    def __init__(self) -> None:
        self.server_address: str = 'localhost'
        self.server_port: int = 55557
        self.buffer: int = 4096
        self.clients = {}

        self.user_name:str = ""
        self.message: str =""

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print('starting up on port {}'.format(self.server_port))
    
    def sock_bind(self) -> None:
        self.sock.bind((self.server_address, self.server_port))


    def recv_data(self) -> None:
        while True:
            try:
                message_byte, address = self.sock.recvfrom(self.buffer)
                print('Connected with{}.'.format(address))
                return message_byte, address
            except Exception as err:
                print('Occured {}'.format(err))
                return None,None
            
    def handle_message(self) -> None:
        message_bytes, client_address = self.recv_data()
        if message_bytes and client_address:
            user_name_length = message_bytes[0]
            user_name = message_bytes[1:1+user_name_length].decode()
            message = message_bytes[1+user_name_length:].decode()
        
        if client_address not in self.clients:
            self.clients[client_address] = Client_info(user_name, client_address)
        self.clients[client_address].last_response = time.time()

        print(f'{user_name}: {message}')
        self.relay_message(message_bytes, client_address)

    def relay_message(self, message_bytes, sender_address) -> None:   
        for client in self.clients.values():
            if client.client_address != sender_address:
                self.sock.sendto(message_bytes, client.client_address)
                print('Sent {} bytes back to {}'.format(len(message_bytes), client.client_address))

    def remove_inactive_user(self) -> None:
        while True:
            current_time = time.time()
            for address in list(self.clients.keys()):
                if current_time - self.clients[address].last_response > 60:
                    del self.clients[address]
            time.sleep(10)
                    

    def sock_close(self) -> None:
        print('closing sock from UDP Server...')
        self.sock.close()

    def chat_start(self) -> None:
        self.sock_bind()
        threading.Thread(target=self.remove_inactive_user).start()

        try:
            while True:
                self.handle_message()
        except Exception as e:
            print('Error occured {}'.format(e))
        finally:
            self.sock_close()



def main():
    udp_server = UDP_Server()
    tcp_server = TCPServer()

    thread_udp = threading.Thread(target=udp_server.chat_start)
    thread_tcp = threading.Thread(target=tcp_server.start)

    thread_tcp.start()
    thread_udp.start()

    thread_tcp.join()
    thread_udp.join()

if __name__ == "__main__":
    main()
