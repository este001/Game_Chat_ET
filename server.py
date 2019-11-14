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
    message = f"S{user} > {message[1:]}".encode('utf-8')
    for c in clients:
        c.sendall(message)


def game_challenge():
    pass


def whisper_message(whispered_message, clients, conn):
    user_to_whisper_list = whispered_message.split()
    user_to_whisper_list = [user.strip('@') for user in user_to_whisper_list if user[0] == '@']
    for c in clients:
        if [True for user in user_to_whisper_list if clients[c] == user]:
            c.sendall(f'{clients[conn]} > {whispered_message}'.encode('utf-8'))


def receive_messages(conn):
    try:
        while True:
            message = conn.recv(1024)
            if not message:
                break
            elif message[0] == "S":
                broadcast_message(message, clients, conn)
            elif message[0] == "C":
                # TODO challange logic
                game_challenge()
            elif '@' in message.decode('utf-8'):
                whisper_message(message.decode('utf-8'), clients, conn)

    except ConnectionResetError as cre:
        print('recieve message:', cre)
        conn.close()
        del clients[conn]


def client_connected(conn):
    while True:
        user_name = conn.recv(1024)
        if not user_name:
            break

        if username_exists(user_name.decode('utf-8'), clients):
            conn.sendall('1'.encode('utf-8'))
        else:
            conn.sendall('0'.encode('utf-8'))
            clients[conn] = user_name.decode('utf-8')
            broadcast_message(message="Shas connected".encode('utf-8'), conn=conn, clients=clients)
            receive_messages(conn)
            break


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
