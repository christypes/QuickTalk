from socket import *


host, port = '18.191.254.249', 5000

# Creates connection socket
# AF_INET: Indicates network as IPv4
# SOCK_STREAM: Indicates socket type as TCP
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect((host, port))  # Initiates 3-way handshake

# Obtains input from user, and drop encoded bytes into the TCP connection
sentence = input('Input lowercase sentence: ')
client_socket.send(sentence.encode())   # converts string into bytes

# Received bytes get placed in "modifiedSentence", and get decoded string
modifiedSentence = client_socket.recv(1024)
print('From Server: ', modifiedSentence.decode())

# Closes the socket, closing the TCP connection.
client_socket.close()



# try:
#     while True:
#         # Send a message to the server
#         message = input("Enter message to send to server: ")
#         if message.lower() == 'exit':
#             print("Disconnecting from server...")
#             break

#         client_socket.send(message.encode())

#         # Receive the server's response
#         response = client_socket.recv(1024)
#         print(f"Received from server: {response.decode()}")

# except KeyboardInterrupt:
#     print("\nClient disconnected.")

# finally:
#     # Close the client socket
#     client_socket.close()
#     print("Client socket closed.")
