import struct
import socket
from enum import Enum

class MessageType(Enum):
    INITIAL_CONNECTION = 0
    MESSAGE = 1
    DISCONNECT = 2
    PASSWORD = 3
    ID = 4

def custom_encode(data):
    return bytes([ord(c) for c in data])

def custom_decode(byte_data):
    return ''.join(chr(b) for b in byte_data)

def send_message(socket: socket.socket, message, message_type: MessageType):
    if not isinstance(message_type, MessageType):
        raise TypeError("message_type must be an instance of MessageType")
    # Encode the message and prepare the length header
    message_bytes = custom_encode(message)
    message_length = len(message_bytes)
    header = struct.pack('!BI', message_type.value, message_length)

    # Send the header and message
    socket.sendall(header)
    socket.sendall(message_bytes)

def receive_message(socket: socket.socket):
    # Receive the header
    header = socket.recv(5)  # 1 byte for type, 4 bytes for length
    if not header:
        return None, None
    message_type_value, message_length = struct.unpack('!BI', header)

    # Convert the message type value back to a MessageType
    try:
        message_type = MessageType(message_type_value)
    except ValueError:
        raise ValueError("Received invalid message type")

    # Receive full message data
    message_data = b''
    while len(message_data) < message_length:
        packet = socket.recv(message_length - len(message_data))
        if not packet:
            break
        message_data += packet

    return custom_decode(message_data), message_type

def is_socket_closed(socket: socket.socket) -> bool:
    try:
        # this will try to read bytes without blocking and also without removing them from buffer (peek only)
        data = socket.recv(16, socket.MSG_DONTWAIT | socket.MSG_PEEK)
        if len(data) == 0:
            return True
    except BlockingIOError:
        return False  # socket is open and reading from it would block
    except ConnectionResetError:
        return True  # socket was closed for some other reason
    except Exception:
        return False
    return False
