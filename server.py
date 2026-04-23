import socket
import threading
import ssl

HOST = '127.0.0.1'
PORT = 12350

clients = []
usernames = []

def broadcast(message):
    for client in clients:
        client.send(message)

def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            if not message:
                break
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            username = usernames[index]
            usernames.remove(username)
            broadcast(f"{username} left the chat".encode())
            client.close()
            break

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print("Server started...")

while True:
    conn, addr = server.accept()
    secure_conn = context.wrap_socket(conn, server_side=True)

    print(f"Connected: {addr}")

    secure_conn.send("USERNAME".encode())
    username = secure_conn.recv(1024).decode()

    usernames.append(username)
    clients.append(secure_conn)

    print(f"Username: {username}")
    broadcast(f"{username} joined the chat".encode())

    thread = threading.Thread(target=handle_client, args=(secure_conn,))
    thread.start()
