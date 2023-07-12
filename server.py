import logging
import socket
import threading
import json

# Configuração do log
logging.basicConfig(filename='chat_server.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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
        try:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            logging.info("Servidor iniciado. Aguardando conexões...")

            while True:
                client_socket, client_address = self.server_socket.accept()
                logging.info(f"Conexão estabelecida com {client_address[0]}:{client_address[1]}")
                self.client_sockets.append(client_socket)
                threading.Thread(target=self.handle_client, args=(client_socket,)).start()
        except socket.error as e:
            logging.error(f"Erro ao iniciar o servidor: {e}")
            self.shutdown()

    def handle_client(self, client_socket):
        try:
            name = client_socket.recv(1024).decode()
            self.client_names.append(name)
            self.broadcast(f"{name} entrou no chat.")

            while True:
                try:
                    message = client_socket.recv(1024).decode()
                    if message:
                        message_data = {"type": "message", "name": name, "message": message}
                        self.messages.append(message_data)  # Salvar a mensagem na lista de mensagens
                        self.save_messages()  # Salvar as mensagens em um arquivo JSON
                        self.broadcast(f"{name}: {message}")
                    else:
                        self.remove_client(client_socket)
                        break
                except (ConnectionResetError, ConnectionAbortedError) as e:
                    logging.error(f"Erro na conexão com o cliente: {e}")
                    self.remove_client(client_socket)
                    break
                except socket.error as e:
                    logging.error(f"Erro no socket: {e}")
                    self.remove_client(client_socket)
                    break
        except socket.error as e:
            logging.error(f"Erro ao lidar com o cliente: {e}")
            self.remove_client(client_socket)

    def broadcast(self, message):
        with self.lock:
            for client_socket in self.client_sockets:
                try:
                    client_socket.send(message.encode())
                except socket.error as e:
                    logging.error(f"Erro ao enviar mensagem para um cliente: {e}")
                    self.remove_client(client_socket)

    def remove_client(self, client_socket):
        with self.lock:
            if client_socket in self.client_sockets:
                index = self.client_sockets.index(client_socket)
                self.client_sockets.remove(client_socket)
                name = self.client_names[index]
                self.client_names.remove(name)
                client_socket.close()
                self.broadcast(f"{name} saiu do chat.")

    def shutdown(self):
        with self.lock:
            for client_socket in self.client_sockets:
                client_socket.close()
            self.server_socket.close()

# Configurações do servidor
HOST = 'localhost'
PORT = 5000

# Iniciando o servidor
server = ChatServer(HOST, PORT)
server.start()
