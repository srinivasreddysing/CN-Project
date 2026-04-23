import socket
import ssl
import threading

HOST = '127.0.0.1'
PORT = 12350

context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
secure_client = context.wrap_socket(client)

secure_client.connect((HOST, PORT))

def receive():
    while True:
        try:
            message = secure_client.recv(1024).decode()
            if message == "USERNAME":
                username = input("Enter your username: ")
                secure_client.send(username.encode())
            else:
                print(message)
        except:
            print("Error!")
            secure_client.close()
            break

def write():
    while True:
        message = input("")
        secure_client.send(message.encode())

threading.Thread(target=receive).start()
threading.Thread(target=write).start()
