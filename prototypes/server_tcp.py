from socket import *

server_port = 5000
server_socket = socket(AF_INET, SOCK_STREAM)    # TCP/UDP (SOCK_DGRAM)
server_socket.bind(('', serverPort))            # TCP/UDP: Opens given port for all IP
server_socket.listen(1)                         # TCP

print("Listening started..")
buffer = 1024
while True:
    connection_socket, client_address = serverSocket.accept()   # TCP, waits for connection
    message = connection_socket.recv(buffer).decode()           # TCP
    # message, client_address = server_socket.recvfrom(buffer)  # UDP
    message = "Received: " + message
    connectionSocket.send(message.encode())                             # TCP
    # server_socket.sendto(modified_message.encode(), client_address)   # UDP
    
    connectionSocket.close()    # TCP