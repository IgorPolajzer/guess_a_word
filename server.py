import socket

server_ip = '127.0.0.1'
server_port = 12345

max_connections = 5

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server_ip, server_port))
server_socket.listen(max_connections)

client_socket, client_address = server_socket.accept()


data = client_socket.recv(1024)
client_socket.send("Hello, Client!".encode())

client_socket.close()
server_socket.close()


