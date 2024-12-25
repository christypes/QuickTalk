from socket import *

server_name, server_port = 'QuickTalk', 5000
client_socket = socket(AF_INET, SOCK_STREAM)     # TCP(SOCK_STREAM) / UDP(SOCK_DGRAM)
client_socket.connect((serverName,serverPort))   # TCP (Omit for UDP) 

message = input('Input message: ')
client_socket.send(sentence.encode())                                # TCP
# client_socket.sendto(message.encode(),(server_name, server_port))  # UDP

buffer = 1024
received_message = client_socket.recv(buffer)                        # TCP
# received_message, serverAddress = client_socket.recvfrom(buffer)   # UDP
print(received_message.decode())

client_socket.close()