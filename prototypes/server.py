from socket import *
import threading
import logging
host, port = '0.0.0.0', 5000
max_queue = 5
buffer_size = 1024

logging.basicConfig(
    filename='server.log',
    level=logging.INFO,
    format='%(asctime)s-%(levelname)s-%(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


# 1. Establishes listening socket
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind((host, port))    # the ip:port on host
server_socket.listen(max_queue)
print('The server is ready to receive')

clients = []  # Lists all connected clinet sockets
client_lock = threading.Lock()

def broadcast(message, sender_socket):
    """Broadcasts message to all connected clients

    Keyword arguments:
    message -- the message sent to broadcast
    sender_socket -- the socket to identify the sender
    """
    with client_lock:
        for client in clients:
            if client != sender_socket:     # Exclude sender itself
                try:
                    client.send(message)
                except:
                    clients.remove(client)  # If unsendable, remove client from the list
                    logging.warning(f'client {client} unreachable, removed from connected clients')
                

# handle_client(): Handles each client
def handle_client(client_socket, addr):
    print(f"Connection with {addr} opened")
    with client_lock:
        clients.append(client_socket)
    client_socket.send("Hello! Welcome to QuickChat!".encode())
    while True:
        message = client_socket.recv(buffer_size)
        if not message:
            print(f"Client {addr} disconnected")
            break
        print(f"Message from {addr}: {message.decode()}")
        broadcast(message, client_socket)
    client_socket.close()
    with client_lock:
        clients.remove(client_socket)
    print(f"Connection with {addr} closed")

while True:
    client_socket, addr = server_socket.accept()                                        # Upon request, creates socket
    client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))  # New thread for each client
    client_thread.start()
