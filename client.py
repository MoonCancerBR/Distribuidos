import socket
import threading

class ChatClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = None

    def start(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))
        print("Conectado ao servidor.")

        client_name = input("Digite seu nome: ")
        self.client_socket.send(client_name.encode())

        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.start()

        while True:
            message = input()
            self.client_socket.send(message.encode())

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode()
                print(message)
            except Exception as e:
                print("Erro:", str(e))
                break

if __name__ == "__main__":
    client = ChatClient('localhost', 5000)
    client.start()
