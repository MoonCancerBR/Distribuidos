import socket
import threading
import json


# Classe para o cliente de chat
class ChatClient:
    def __init__(self, host, port):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((host, port))

    def send_message(self):
        while True:
            message = input()
            message_data = {"type": "message", "message": message}
            message_json = json.dumps(message_data)
            self.client_socket.send(message_json.encode())

    def receive_message(self):
        while True:
            message_json = self.client_socket.recv(1024).decode()
            message_data = json.loads(message_json)
            message_type = message_data["type"]
            if message_type == "join":
                name = message_data["name"]
                print(f"{name} entrou no chat.")
            elif message_type == "message":
                name = message_data["name"]
                message = message_data["message"]
                print(f"{name}: {message}")


# Configurações do cliente
HOST = 'localhost'
PORT = 5000

# Conectando ao servidor
name = input("Digite seu nome: ")
client = ChatClient(HOST, PORT)
client.client_socket.send(name.encode())

# Iniciando as threads para enviar e receber mensagens
send_thread = threading.Thread(target=client.send_message)
receive_thread = threading.Thread(target=client.receive_message)

send_thread.start()
receive_thread.start()
