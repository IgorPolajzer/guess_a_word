import socket

server_ip = '127.0.0.1'
server_port = 12345

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_ip, server_port))

message = "Hello, Server!"
client_socket.send(message.encode())
data = client_socket.recv(1024)
print(f"Received: {data.decode()}")

client_socket.close()
