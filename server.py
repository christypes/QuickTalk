from socket import *
host, port = '0.0.0.0', 5000

# 1. Establishes listening socket
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind((host, port))    # the ip:port on host
server_socket.listen(5)             # Specifies max queue
print('The server is ready to receive')

# 2. Waits for TCP request
try: 
    while True:
        # When request is made, creates client specific socket
        client_socket, addr = server_socket.accept()
        print("3-way handshake complete: ", client_socket, addr)
        try:
            while True:
                message = client_socket.recv(1024)  # buffer_size = 1024
                if not message:
                    print("client disconnected")
                    break
                print(f"Message: {message.decode()}")
                client_socket.send(message.decode().upper().encode())
        except KeyboardInterrupt:
            print("Server shutting down")

        finally:
            # Closes connection but listening socket remains open
            client_socket.close()
            print("Gracefully shut down")

except KeyboardInterrupt:
    print("Server shutting down")
