import socket
import threading
import json

# Classe para o servidor de chat
class ChatServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_sockets = []
        self.client_names = []
        self.lock = threading.Lock()
        self.messages = []  # Inicialização da lista de mensagens

    def save_messages(self):
        with open("chat_messages.json", "w") as file:
            json.dump(self.messages, file, indent=4)

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print("Servidor iniciado. Aguardando conexões...")

        while True:
            client_socket, client_address = self.server_socket.accept()
            print(f"Conexão estabelecida com {client_address[0]}:{client_address[1]}")
            self.client_sockets.append(client_socket)
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

    def handle_client(self, client_socket):
        name = client_socket.recv(1024).decode()
        self.client_names.append(name)
        self.broadcast({"type": "join", "name": name})

        while True:
            try:
                message = client_socket.recv(1024).decode()
                if message:
                    message_data = {"type": "message", "name": name, "message": message}
                    self.messages.append(message_data)  # Salvar a mensagem na lista de mensagens
                    self.save_messages()  # Salvar as mensagens em um arquivo JSON
                    self.broadcast(message_data)
                else:
                    self.remove_client(client_socket)
                    break
            except:
                self.remove_client(client_socket)
                break

    def broadcast(self, message):
        with self.lock:
            message_json = json.dumps(message)
            for client_socket in self.client_sockets:
                client_socket.send(message_json.encode())

    def remove_client(self, client_socket):
        with self.lock:
            if client_socket in self.client_sockets:
                index = self.client_sockets.index(client_socket)
                self.client_sockets.remove(client_socket)
                name = self.client_names[index]
                self.client_names.remove(name)
                client_socket.close()
                self.broadcast(f"{name} saiu do chat.")

# Configurações do servidor
HOST = 'localhost'
PORT = 5000

# Iniciando o servidor
server = ChatServer(HOST, PORT)
server.start()
