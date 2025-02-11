import tkinter as tk
from tkinter import scrolledtext, messagebox
import threading
import json
from socket import *

# Server details
host, port = '18.219.122.122', 5000

# Global socket variable
client_socket = None

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
            received = client_socket.recv(1024)
            if received:
                message = received.decode()
                chat_display.config(state=tk.NORMAL)
                chat_display.insert(tk.END, f"Chris: {message}\n")
                chat_display.config(state=tk.DISABLED)
                chat_display.yview(tk.END)
        except Exception as e:
            print("Error receiving message:", e)
            break

# Function to handle login
def login():
    username = username_entry.get()
    password = password_entry.get()

    if not username or not password:
        messagebox.showerror("Error", "Please enter both username and password")
        return

    # Send login request to the server
    login_data = json.dumps({"username": username, "password": password})
    client_socket.send(login_data.encode())

    # Receive response from the server
    response = client_socket.recv(1024).decode()
    response_data = json.loads(response)

    if response_data.get("status") == "success":
        messagebox.showinfo("Success", "Login successful!")
        login_window.destroy()
        open_chat_window()
    else:
        messagebox.showerror("Error", response_data.get("message", "Login failed"))

# Function to open the chat window
def open_chat_window():
    global chat_display, message_entry

    # Set up the Tkinter window
    root = tk.Tk()
    root.title("QuickChat")
    root.geometry("400x360")

    # Create a ScrolledText widget for the chat display area
    chat_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=20, state=tk.DISABLED)
    chat_display.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

    # Create an Entry widget for typing messages
    message_entry = tk.Text(root, width=40, height=4)
    message_entry.grid(row=1, column=0)

    # Create a Button widget for sending messages
    send_button = tk.Button(root, text="Send", width=2, command=send_message)
    send_button.grid(row=1, column=1, stick="ew")

    # Start the Tkinter main loop
    receive_thread = threading.Thread(target=receive_message, daemon=True)
    receive_thread.start()

    root.mainloop()

# Function to initialize the login window
def init_login_window():
    global login_window, username_entry, password_entry

    login_window = tk.Tk()
    login_window.title("Login")
    login_window.geometry("300x150")

    # Username label and entry
    tk.Label(login_window, text="Username:").grid(row=0, column=0, padx=10, pady=10)
    username_entry = tk.Entry(login_window)
    username_entry.grid(row=0, column=1, padx=10, pady=10)

    # Password label and entry
    tk.Label(login_window, text="Password:").grid(row=1, column=0, padx=10, pady=10)
    password_entry = tk.Entry(login_window, show="*")
    password_entry.grid(row=1, column=1, padx=10, pady=10)

    # Login button
    login_button = tk.Button(login_window, text="Login", command=login)
    login_button.grid(row=2, column=0, columnspan=2, pady=10)

    login_window.mainloop()

# Main function to start the application
def main():
    global client_socket

    # Creates connection socket
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((host, port))  # Initiates 3-way handshake

    # Initialize the login window
    init_login_window()

if __name__ == "__main__":
    main()