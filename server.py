import socket
import os

# Configurações do servidor
HOST = '127.0.0.1'  # Endereço IP do servidor
PORT = 12345  # Porta para escutar as conexões

# Diretório onde os arquivos serão armazenados
SAVE_DIR = 'arquivos'

# Cria o diretório de armazenamento, se não existir
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

# Cria um socket TCP/IP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Associa o socket ao endereço e porta do servidor
sock.bind((HOST, PORT))

# Aguarda por conexões
sock.listen(1)
print(f"Aguardando conexões na porta {PORT}...")

while True:
    # Espera por uma conexão
    conn, addr = sock.accept()
    print(f"Conexão estabelecida com {addr[0]}:{addr[1]}")

    # Recebe o nome do arquivo
    filename = conn.recv(1024).decode()
    filepath = os.path.join(SAVE_DIR, filename)

    # Recebe e armazena o arquivo
    with open(filepath, 'wb') as file:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            file.write(data)

    print(f"Arquivo '{filename}' recebido e armazenado.")

    # Fecha a conexão com o cliente
    conn.close()
