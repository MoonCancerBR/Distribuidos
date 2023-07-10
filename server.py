import socket
import threading

class ChatServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.clients = []
        self.server_socket = None

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print("Chat server started on {}:{}".format(self.host, self.port))

        while True:
            client_socket, client_address = self.server_socket.accept()
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_thread.start()

    def handle_client(self, client_socket):
        client_name = client_socket.recv(1024).decode()
        self.broadcast("{} entrou no chat.".format(client_name))

        self.clients.append((client_name, client_socket))

        while True:
            try:
                message = client_socket.recv(1024).decode()
                if message:
                    self.broadcast("{}: {}".format(client_name, message))
            except Exception as e:
                print("Erro:", str(e))
                self.clients.remove((client_name, client_socket))
                self.broadcast("{} saiu do chat.".format(client_name))
                break

    def broadcast(self, message):
        for _, client_socket in self.clients:
            client_socket.send(message.encode())

if __name__ == "__main__":
    server = ChatServer('localhost', 5000)
    server.start()
