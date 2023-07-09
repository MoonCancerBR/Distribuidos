import socket

# Configurações do cliente
HOST = '127.0.0.1'  # Endereço IP do servidor
PORT = 12345  # Porta do servidor

# Caminho completo do arquivo que será enviado
FILE_PATH = '/caminho/completo/do/arquivo.txt'

# Conecta-se ao servidor
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

# Envia o nome do arquivo
filename = FILE_PATH.split('/')[-1]
sock.sendall(filename.encode())

# Envia o arquivo
with open(FILE_PATH, 'rb') as file:
    while True:
        data = file.read(1024)
        if not data:
            break
        sock.sendall(data)

print(f"Arquivo '{filename}' enviado com sucesso.")

# Fecha a conexão com o servidor
sock.close()
