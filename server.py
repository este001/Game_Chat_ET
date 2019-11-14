"""Server for game/chat"""

import socket
import threading


def username_exists(user_name):
    if user_name in clients.values():
        return True


def client_connected(conn):
    while True:
        user_name = conn.recv(1024)

        if not user_name:
            break
        if username_exists(user_name):
            conn.sendall('0'.encode('utf-8'))


if __name__ == '__main__':
    IP = "127.0.0.1"
    PORT = 1234

    clients = {}

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP, PORT))
    server_socket.listen()

    while True:
        conn, addr = server_socket.accept()

        client_thread = threading.Thread(target=client_connected, args=(conn,))
        client_thread.start()
