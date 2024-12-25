import tkinter as tk
from tkinter import scrolledtext

####
from socket import *
host, port = '18.191.254.249', 5000

# Creates connection socket
# AF_INET: Indicates network as IPv4
# SOCK_STREAM: Indicates socket type as TCP
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect((host, port))  # Initiates 3-way handshake


# Function to handle sending messages
def send_message():
    message = message_entry.get("1.0", tk.END).strip()
    print(message)
    if message != "":
        chat_display.config(state=tk.NORMAL)
        chat_display.insert(tk.END, f"You: {message}\n")
        chat_display.config(state=tk.DISABLED)
        message_entry.delete("1.0", tk.END)
        # *** Here you can send the message to the server
        client_socket.send(message.encode())
        received = client_socket.recv(1024)
        receive_message(received.decode())

# Function to handle receiving messages
def receive_message(message):
    chat_display.config(state=tk.NORMAL)
    chat_display.insert(tk.END, f"Server: {message}\n")
    chat_display.config(state=tk.DISABLED)
    chat_display.yview(tk.END)  # Automatically scroll down to the latest message

# Function to simulate receiving a message from the server
def simulate_server_message():
    receive_message("Hello! Welcome to QuickChat!")

# Set up the Tkinter window
root = tk.Tk()
root.title("QuickChat")
root.geometry("400x360")  # Set the window size

# Create a ScrolledText widget for the chat display area
chat_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=20, state=tk.DISABLED)
chat_display.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

# Create an Entry widget for typing messages
message_entry = tk.Text(root, width=40, height=4)
message_entry.grid(row=1, column=0) #, sticky="ew", padx=2, pady=2)

# Create a Button widget for sending messages
send_button = tk.Button(root, text="Send", width=2, command=send_message)
send_button.grid(row=1, column=1, stick="ew")

# Start the Tkinter main loop
root.after(3000, simulate_server_message)  # Simulate receiving a message every 3 seconds
root.mainloop()

