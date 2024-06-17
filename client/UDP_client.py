import socket
import threading

class UDP_Client:
    def __init__(self, server_address: str, server_port: int, client_address: str, client_port: int, user_name: str) -> None:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_address = server_address
        self.server_port = server_port
        self.client_address = client_address
        self.client_port = client_port
        self.user_name = user_name

        
    def bind_socket(self)-> None:
        self.sock.bind((self.client_address, self.client_port))
            
    def sent_data(self)->None:
        print('Enter message: ')
        while True:
            message:str  = input('')
            if message == 'exit':
                break

            sent_byte:bytes = f"{self.username}: {message}.encode()"
            self.sock.sendto(sent_byte,(self.server_address,self.server_port))


    def recv_data(self):
        while True:
            recieved_data, _ = self.sock.recvfrom(4096)
            recieved_message_data = recieved_data.decode()
            
 
    def closing_socket(self)->None:
        self.sock.socket()


    def chat_start(self)-> None:
        self.bind_socket()

        try:
            print('start chating... ')
            thread_sent = threading.Thread(target = self.sent_data)
            thread_recived = threading.Thread(target = self.recv_data)

            thread_sent.start()
            thread_recived.start()

            # join
            thread_sent.join()
            thread_recived.join()

        finally:
            self.closing_socket()

def main() -> None:
    client_address = ''
    client_port = 9050
    server_address = '127.0.0.1'
    server_port = 9999
    user_name = input('Enter your name -> ')
    UDP_Client_chat = UDP_Client(client_address, client_port, server_address, server_port, user_name)
    UDP_Client_chat.chat_start()

if __name__ == "__main__":
    main()
    

