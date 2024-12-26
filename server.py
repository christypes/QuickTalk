from socket import *
import thread # ***
host, port = '0.0.0.0', 5000
max_queue = 5

# 1. Establishes listening socket
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind((host, port))    # the ip:port on host
server_socket.listen(max_queue)
print('The server is ready to receive')

# 2. Waits for TCP request
from socket import *
import threading  # *** Import threading module

host, port = '0.0.0.0', 5000

# 1. Establishes listening socket
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind((host, port))    # the ip:port on host
server_socket.listen(5)             # Specifies max queue
print('The server is ready to receive')

# 2. List of all connected client sockets
clients = []  # *** List to hold all connected clients

def broadcast(message, sender_socket):  # *** Function to broadcast message to all clients
    for client in clients:  # *** Loop through all clients
        if client != sender_socket:  # *** Don't send the message to the sender
            try:
                client.send(message)
            except:
                clients.remove(client)  # *** Remove client if it can't send a message

def handle_client(client_socket, addr):  # *** Define a function to handle each client
    print("3-way handshake complete: ", client_socket, addr)
    clients.append(client_socket)  # *** Add client to the list of connected clients
    client_socket.send("Hello! Welcome to QuickChat!".encode())
    while True:
        message = client_socket.recv(1024)  # buffer_size = 1024
        if not message:
            print(f"Client {addr} disconnected")
            break
        print(f"Message from {addr}: {message.decode()}")
        broadcast(message, client_socket)  # *** Broadcast the received message to all clients
    # Closes connection but listening socket remains open
    client_socket.close()
    clients.remove(client_socket)  # *** Remove client from the list
    print(f"Connection with {addr} closed")

while True:
    # When request is made, creates client specific socket
    client_socket, addr = server_socket.accept()
    # Create a new thread for each client
    client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))  # *** Create thread
    client_thread.start()  # *** Start the thread


# try: 
#     while True:
#         # When request is made, creates client specific socket
#         client_socket, addr = server_socket.accept()
#         print("3-way handshake complete: ", client_socket, addr)
#         try:
#             while True:
#                 message = client_socket.recv(1024)  # buffer_size = 1024
#                 if not message:
#                     print("client disconnected")
#                     break
#                 print(f"Message: {message.decode()}")
#                 client_socket.send(message.decode().upper().encode())
#         except KeyboardInterrupt:
#             print("Server shutting down")

#         finally:
#             # Closes connection but listening socket remains open
#             client_socket.close()
#             print("Gracefully shut down")

# except KeyboardInterrupt:
#     print("Server shutting down")
