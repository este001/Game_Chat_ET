import socket
import threading


def username_exists(user_name, clients):
    if user_name in clients.values():
        return True
    else:
        return False


def broadcast_message(message, clients, conn):

    message = message.decode('utf-8')
    user = clients[conn]
    message = f"{user + ' > ' + message}".encode('utf-8')

    for c in clients:
        c.sendall(message)


def receive_messages(conn):
    try:
        while True:
            message = conn.recv(1024)
            if not message:
                break
            broadcast_message(message, clients, conn)

    except ConnectionResetError as cre:
        print('recieve message:', cre)
        conn.close()
        del clients[conn]


def client_connected(conn):
    while True:
        user_name = conn.recv(1024).decode('utf-8')
        if not user_name:
            break

        if username_exists(user_name, clients):
            conn.sendall('1'.encode('utf-8'))
        else:
            conn.sendall('0'.encode('utf-8'))
            clients[conn] = user_name
            receive_messages(conn)


if __name__ == '__main__':
    IP = "127.0.0.1"
    PORT = 1234

    # Dictionary for clients connected
    clients = {}

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP, PORT))
    server_socket.listen()

    while True:
        conn, addr = server_socket.accept()

        client_thread = threading.Thread(target=client_connected, args=(conn,), daemon=True)
        client_thread.start()
