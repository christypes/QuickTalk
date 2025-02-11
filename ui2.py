from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QListWidget, QHBoxLayout
from PyQt6.QtCore import Qt, QThread, pyqtSignal
import socket
import json
import sys

# Server details
SERVER_HOST = '18.219.122.122'
SERVER_PORT = 5000

class ChatClient(QThread):
    message_received = pyqtSignal(str)  # communicate between objects.
    def __init__(self, username, token):
        super().__init__()
        self.username, self.token = username, token
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((SERVER_HOST, SERVER_PORT))
    def run(self):     # Continously listens for message reception
        while True:
            try:
                message = self.client_socket.recv(1024).decode()
                if message:
                    self.message_received.emit(message)
            except:
                break
    def send_message(self, message):
        self.client_socket.send(message.encode())

# GUI Logic
class LoginScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.move(self.screen().geometry().center() - self.rect().center())
        layout = QVBoxLayout()
        
        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Username")
        layout.addWidget(self.username_input)
        
        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_input)
        
        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.login)
        layout.addWidget(self.login_button)
        
        self.register_button = QPushButton("Register")
        self.register_button.clicked.connect(self.register)
        layout.addWidget(self.register_button)
        
        self.error_label = QLabel("", self)
        layout.addWidget(self.error_label)
        
        self.setLayout(layout)
    
    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        # Here, add authentication logic (send to backend, receive JWT, etc.)
        self.chat_window = ChatScreen(username, "dummy_token")  # Replace with real token
        self.chat_window.show()
        self.close()
    
    def register(self):
        pass  # Implement registration logic

class ChatScreen(QWidget):
    def __init__(self, username, token):
        super().__init__()
        self.setWindowTitle("Chat Room")
        self.move(self.screen().geometry().center() - self.rect().center())
        self.username = username
        self.token = token
        
        layout = QVBoxLayout()
        
        self.chat_display = QTextEdit(self)
        self.chat_display.setReadOnly(True)
        layout.addWidget(self.chat_display)
        
        self.message_input = QLineEdit(self)
        self.message_input.setPlaceholderText("Type a message...")
        layout.addWidget(self.message_input)
        
        send_button = QPushButton("Send")
        send_button.clicked.connect(self.send_message)
        layout.addWidget(send_button)
        
        self.private_chat_button = QPushButton("Start Private Chat")
        self.private_chat_button.clicked.connect(self.start_private_chat)
        layout.addWidget(self.private_chat_button)
        
        self.setLayout(layout)
        
        self.client = ChatClient(username, token)
        self.client.message_received.connect(self.display_message)
        self.client.start()
    
    def display_message(self, message):
        self.chat_display.append(message)
    
    def send_message(self):
        message = self.message_input.text()
        if message:
            self.client.send_message(f"{self.username}: {message}")
            self.message_input.clear()
    
    def start_private_chat(self):
        user_id, ok = QInputDialog.getText(self, "Private Chat", "Enter user ID:")
        if ok and user_id:
            self.chat_display.append(f"Starting private chat with {user_id}...")
            # Implement private chat connection logic

if __name__ == "__main__":
    app = QApplication(sys.argv)
    login = LoginScreen()
    login.show()
    sys.exit(app.exec())
