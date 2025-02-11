import tkinter as tk
from tkinter import scrolledtext
import threading

from socket import *

host, port = '18.219.122.122', 5000

# Creates connection socket
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect((host, port))  # Initiates 3-way handshake

# Function to handle sending messages
def send_message():
    message = message_entry.get("1.0", tk.END).strip()
    if message != "":
        chat_display.config(state=tk.NORMAL)
        chat_display.insert(tk.END, f"You: {message}\n")
        chat_display.config(state=tk.DISABLED)
        message_entry.delete("1.0", tk.END)
        client_socket.send(message.encode())

# Function to handle receiving messages
def receive_message():
    while True:
        try:
            received = client_socket.recv(1024)  # Receive data from server
            if received:
                message = received.decode()
                chat_display.config(state=tk.NORMAL)
                chat_display.insert(tk.END, f"Chris: {message}\n")
                chat_display.config(state=tk.DISABLED)
                chat_display.yview(tk.END)  # Automatically scroll down to the latest message
        except Exception as e:
            print("Error receiving message:", e)
            break

# Function to simulate receiving a message from the server
def simulate_server_message():
    receive_message("Hello! Welcome to QuickChat!")

# Set up the Tkinter window
root = tk.Tk()
root.title("QuickChat")
root.geometry("400x360")  # Set the window size

# Create frames for login and registration
login_frame = tk.Frame(root)
register_frame = tk.Frame(root)
chat_frame = tk.Frame(root)

# Login Form
tk.Label(login_frame, text="Username").grid(row=0, column=0)
username_entry = tk.Entry(login_frame)
username_entry.grid(row=0, column=1)

tk.Label(login_frame, text="Password").grid(row=1, column=0)
password_entry = tk.Entry(login_frame, show="*")
password_entry.grid(row=1, column=1)

login_button = tk.Button(login_frame, text="Login", command=lambda: login(username_entry.get(), password_entry.get()))
login_button.grid(row=2, columnspan=2)

error_label = tk.Label(login_frame, fg="red")
error_label.grid(row=3, columnspan=2)

register_button = tk.Button(login_frame, text="Register", command=lambda: switch_to_register())
register_button.grid(row=4, columnspan=2)

# Register Form
tk.Label(register_frame, text="Username").grid(row=0, column=0)
username_entry = tk.Entry(register_frame)
username_entry.grid(row=0, column=1)

tk.Label(register_frame, text="Password").grid(row=1, column=0)
password_entry = tk.Entry(register_frame, show="*")
password_entry.grid(row=1, column=1)

register_button = tk.Button(register_frame, text="Register", command=lambda: register(username_entry.get(), password_entry.get()))
register_button.grid(row=2, columnspan=2)

# Chat window (hidden initially)
chat_display = scrolledtext.ScrolledText(chat_frame, wrap=tk.WORD, width=50, height=20, state=tk.DISABLED)
chat_display.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

message_entry = tk.Text(chat_frame, width=40, height=4)
message_entry.grid(row=1, column=0)

send_button = tk.Button(chat_frame, text="Send", command=send_message)
send_button.grid(row=1, column=1)

# Switch to register frame
def switch_to_register():
    login_frame.grid_forget()
    register_frame.grid(row=0, column=0)

# Function to handle login (this should be connected to the server, for now just UI)
def login(username, password):
    print(f"Logging in with Username: {username} and Password: {password}")
    # Here, you would add server communication for authentication

    # On successful login, hide login and show chat
    login_frame.grid_forget()
    chat_frame.grid(row=0, column=0)
    receive_thread = threading.Thread(target=receive_message, daemon=True)
    receive_thread.start()

# Function to handle registration (this should be connected to the server, for now just UI)
def register(username, password):
    print(f"Registering Username: {username} and Password: {password}")
    # Here, you would add server communication for registration
    

    # On successful registration, show login frame again
    register_frame.grid_forget()
    login_frame.grid(row=0, column=0)

# Start with login frame
login_frame.grid(row=0, column=0)

root.mainloop()
