import socket
import uuid
from utils import send_message, receive_message, MessageType
from secrets import server_password

server_ip = '127.0.0.1'
server_port = 12345

max_connections = 5

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server_ip, server_port))
server_socket.listen(max_connections)

print(f"Server listening on {server_ip}:{server_port}")

try:
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}")
        send_message(client_socket, "Hello, player!", MessageType.INITIAL_CONNECTION)

        try:
            while True:
                message, message_type = receive_message(client_socket)
                if message:
                    if message_type == MessageType.INITIAL_CONNECTION:
                        print(f'Received response: {message}')
                    elif message_type == MessageType.PASSWORD:
                        if message == server_password:
                            print(f"Password '{message}' is correct.")
                            send_message(client_socket, "Password is correct!", MessageType.PASSWORD)
                            send_message(client_socket, str(uuid.uuid4()), MessageType.ID)
                        else:
                            print(f"Password '{message}' is incorrect.")
                            send_message(client_socket, "Password is incorrect. Disconnecting...", MessageType.DISCONNECT)
                            break  # Exit the loop to disconnect the client
                    elif message_type == MessageType.MESSAGE:
                        print(f"Received message from client: {message}")
                    elif message_type == MessageType.ID:
                        print(f"Received ID from client: {message}")

        except ConnectionError:
            print(f"Connection closed by client {client_address}")
        except Exception as e:
            print(f"Error in client {client_address}: {e}")

        finally:
            client_socket.close()

except Exception as e:
    print(f"Server error: {e}")

finally:
    server_socket.close()
