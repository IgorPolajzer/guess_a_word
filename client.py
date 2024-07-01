import socket
import sys
import uuid
from utils import send_message, receive_message, MessageType
from secrets import server_password

server_ip = '127.0.0.1'
server_port = 12345

try:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))

    message = "Hello, Server!"
    send_message(client_socket, message, MessageType.INITIAL_CONNECTION)

    while True:
        response, message_type = receive_message(client_socket)
        if response:
            if message_type == MessageType.INITIAL_CONNECTION:
                print(f'Received response: {response}')
                password = input("Enter password: ")
                send_message(client_socket, password, MessageType.PASSWORD)
            elif message_type == MessageType.MESSAGE:
                print(response)
            elif message_type == MessageType.PASSWORD:
                print(response)
            elif message_type == MessageType.ID:
                print(f'Your assigned ID is: {response}')
            elif message_type == MessageType.DISCONNECT:
                print(response)
                sys.exit(0)

except ConnectionError:
    print("Connection to server closed.")
except Exception as e:
    print(f"Error: {e}")

finally:
    client_socket.close()
