import socket
import threading
import time

class Client_info:
    def __init__(self, user_name, client_address):
        self.user_name = user_name
        self.client_address = client_address
        self.last_response = time.time()

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
                self.message = message_byte.decode()
                return message_byte, address
            except Exception as err:
                print('occured {}'.format(err))
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
        self.send(message_bytes, client_address)

    def send(self, message_bytes, address) -> None:
        if message_bytes:
            for client in self.clients.values():
                if client.client_address != address:
                    self.sock.sendto(message_bytes, client.client_address)
                    print('Sent {} bytes back to {}'.format(len(message_bytes),client.client_address))

    def remove_inactive_user(self) -> None:
        while True:
            current_time = time.time()
            for address in list(self.clients.keys()):
                if current_time - self.clients[address].last_response > 60:
                    del self.clients[address]
            time.sleep(10)
                    

    def sock_close(self) -> None:
        print('closing sock from UDP_Server...')
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
    thread_udp = threading.Thread(target=udp_server.chat_start)
    thread_udp.start()
    thread_udp.join()

if __name__ == "__main__":
    main()
