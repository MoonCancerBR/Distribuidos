import logging
import socket
import threading

# Classe para o cliente de chat
class ChatClient:
    def __init__(self, host, port):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((host, port))

    def send_message(self):
        while True:
            try:
                message = input()
                self.client_socket.send(message.encode())
            except socket.error as e:
                logging.error(f"Erro ao enviar mensagem para o servidor: {e}")
                self.shutdown()

    def receive_message(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode()
                print(message)
            except socket.error as e:
                logging.error(f"Erro ao receber mensagem do servidor: {e}")
                self.shutdown()

    def shutdown(self):
        self.client_socket.close()

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
