import socket
import threading
import struct
import json
import time
import random
import string
import re
import uuid

class ClientInfo:
    def __init__(self, user_name, client_address):
        self.user_name = user_name
        self.client_address = client_address
        self.last_response = time.time()


class memberInfo:
    def __init__(self, client_token: str = "", user_name: str = "", ip_address : str = "") -> None:
        self.client_token = client_token
        self.user_name = user_name
        self.ip_address = ip_address

class hostInfo:
    def __init__(self, host_token: str = "", room_name: str = "", room_name_size: int = 0,  user_name: str = "", ip_address: str = "") -> None:
        self.host_token = host_token
        self.room_name = room_name
        self.room_name_size = room_name_size
        self.user_name = user_name
        self.ip_address = ip_address

class ChatRoom:
    clients: list[memberInfo] = []

    def __init__(self, host_user: hostInfo = hostInfo()) -> None:
        self.host_user = host_user

    def add_user(self, user: memberInfo) -> None:
        self.clients.append(user)


class ChatRoomManager:
    chat_rooms: list[ChatRoom] = []

    def __init__(self) -> None:
        pass

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



class TCPServer:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address: str = '127.0.0.1'
        self.server_port: int = 55557
        self.buffer:int = 32

        self.room_name_size: int = 1
        self.operation: int = 1
        self.state: int = 0
        self.operation_payload_size:int = 29 #include the content of the message 
        self.room_name: str = ""
        self.passwords: str = ""
        self.host_token: str = ""
        self.user_name: str = ""


        self.clients = []
        self.chat_rooms = []
        self.chat_room = {}

        self.sock.bind((self.server_address, self.server_port))
        print('TCP SERVER start up on {}, port {}'.format(self.server_address, self.server_port))
        self.sock.listen(1)

    def head_init(self,head: bytes) -> None:
        handle_head = HandleHead()
        handle_head.get_size(head)

    def initialize_defaults(self):
        self.room_name_size = 1
        self.operation = 1
        self.state = 0
        self.room_name = ''
        self.host_token = ''
        self.user_name = ''

    
    def create_head(self):
        room_name_size_bytes: bytes = self.room_name_size.to_bytes(1, byteorder='big')
        operation_bytes: bytes = self.operation.to_bytes(1, byteorder='big')
        state_bytes: bytes = self.state.to_bytes(1, byteorder='big')
        operation_payload_size_bytes: bytes = self.operation_payload_size.to_bytes(29, byteorder='big')

        header = room_name_size_bytes + operation_bytes + state_bytes + operation_payload_size_bytes

        return header

    def chat_start(self):
        while True:
            connection, client_address = self.sock.accept()
            try:
                while True:
                    print('TCP SERVER from {}'.format(client_address))

                    self.head_init(connection.recv(self.buffer))
                
                    print(f"Operation: {self.operation}")

                    if self.operation == 1:
                        print("Operation is 1, processing...")
                        self.state = 1
                        
                        try:
                            connection.send(self.create_head())
                        except socket.error as e:
                            print(f"Error sending data: {e}")
                            break
                        
                        

                        self.host_token = str(uuid.uuid4())

                        host_user = hostInfo(self.host_token,
                                            self.room_name,
                                            self.room_name_size,
                                            self.user_name,
                                            self.server_address)

                        chat_room = ChatRoom(host_user)
                        chat_room_manager.chat_rooms.append(chat_room)

                        self.state = 2

                        connection.send(self.create_head())
                        connection.send(self.host_token.encode())
                        connection.send(host_user_list.ip_address.encode())

                        break

                    elif self.operation == 2:
                        connection.send('TOKEN'.encode())
                        user_token = connection.recv(36) #uuidの関係
                        if self.host_token == user_token:
                            chat_member_user = memberInfo(user_token,
                                                            self.user_name,
                                                            self.server_address)

                            chat_room_list = ChatRoom()
                            chat_room_list.add_user(chat_member_user)

                            client_ip_address = chat_member_user.server_address

                            connection.send(client_ip_address.encode())

                        break
                    
                    self.initialize_defaults()
            
            except socket.error as e:
                print('TCP SERVER occured {} in a method of chat start'.format(e))
                return

            finally:
                connection.close()
    
    # def chat_start(self) -> None:
        while True:
            connection, client_address = self.sock.accept()
            try:
                while True:
                    print('TCP SERVER from {}'.format(client_address))

                    self.head_init(connection.recv(self.buffer))

                    print(f"Operation: {self.operation}")

                    if self.operation == 1:
                        print("Operation is 1, processing...")
                        self.state = 1

                        connection.send(self.create_head())

                        self.host_token = str(uuid.uuid4())

                        host_user = hostInfo(self.host_token,
                                            self.room_name,
                                            self.room_name_size,
                                            self.user_name,
                                            self.server_address)

                        chat_room = ChatRoom(host_user)
                        self.chat_room_manager.add_room(chat_room)  # self.chat_room_managerを使用

                        self.state = 2

                        connection.send(self.create_head())
                        connection.send(self.host_token.encode())
                        connection.send(host_user.ip_address.encode())  # host_userを使用

                        break

                    elif self.operation == 2:
                        connection.send('TOKEN'.encode())
                        user_token = connection.recv(36)  # uuidの関係
                        if self.host_token == user_token.decode():
                            chat_member_user = memberInfo(user_token.decode(),
                                                          self.user_name,
                                                          self.server_address)

                            # 既存のチャットルームにユーザーを追加
                            for room in self.chat_room_manager.chat_rooms:
                                if room.host_user.host_token == self.host_token:
                                    room.add_user(chat_member_user)
                                    client_ip_address = chat_member_user.ip_address
                                    connection.send(client_ip_address.encode())
                                    break

                        break

                    self.initialize_defaults()

            except Exception as e:
                print('TCP SERVER occurred {}'.format(e))

            finally:
                connection.close()

    def close_sock(self) -> None:
        print("TCP SERVER closing...")
        self.sock.close()





class UDPServer:
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
            self.clients[client_address] = ClientInfo(user_name, client_address)
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

chat_room_manager: ChatRoomManager = ChatRoomManager()
host_user_list : hostInfo = hostInfo()
chat_member_user: memberInfo = memberInfo()
chat_room: ChatRoom = ChatRoom()


def main():
    
    tcp_server = TCPServer()
    udp_server = UDPServer()
    

    thread_tcp = threading.Thread(target=tcp_server.chat_start)
    thread_udp = threading.Thread(target=udp_server.chat_start)
    

    thread_tcp.start()
    thread_udp.start()

    thread_tcp.join()
    thread_udp.join()

if __name__ == "__main__":
    main()

