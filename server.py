import socket
import threading
import time


def send_message(message, clients):
    for c in clients:
        c.sendall(message.encode('utf'))


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


def player_accepted_challenge(clients, name, conn):
    pass


def player_declined_challenge(clients, name, conn):
    player_game_status[clients[conn]] = True
    player_game_status[name] = True
    message = f"{clients[conn]} has declined a challenge from {name}"
    send_message(message, clients)


def player_availability(player):
    if player_game_status[player]:
        return True
    else:
        return False


def game_challenge(conn, message, clients):
    message = message.decode('utf-8')
    challenger = clients[conn]
    player_game_status[clients[conn]] = False
    player_to_challenge = message[1:]

    if player_availability(player_to_challenge):
        player_game_status[player_to_challenge] = False
        for c in clients:
            if clients[c] == player_to_challenge:
                c.sendall(f'C{challenger}'.encode('utf-8'))
    else:
        player_game_status[clients[conn]] = True
        conn.sendall(f'D'.encode('utf-8'))


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

            elif message[0:1].decode('utf-8') == "S":
                broadcast_message(message, clients, conn)

            elif message[0:1].decode('utf-8') == "C":
                # TODO challenge logic
                game_challenge(conn, message, clients)

            elif message[0:1].decode('utf-8') == "D":
                message = message[0:1].decode('utf-8')
                player_declined_challenge(clients, message, conn)

            elif '@' in message.decode('utf-8'):
                whisper_message(message.decode('utf-8'), clients, conn)

    except ConnectionResetError as cre:
        print('receive message', cre)
        conn.close()
        del clients[conn]
        send_message(online_users(clients), clients)


def online_users(clients):
    users_online = "O"
    for c in clients:
        users_online += clients[c] + '-'
    return users_online


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
            player_game_status[user_name.decode('utf-8')] = True
            broadcast_message(message="Shas connected".encode('utf-8'), conn=conn, clients=clients)
            time.sleep(1)
            send_message(online_users(clients), clients)
            receive_messages(conn)
            break


if __name__ == '__main__':
    IP = "127.0.0.1"
    PORT = 1234

    # Dictionary for clients connected
    clients = {}
    # Dict for player challenge status
    player_game_status = {}

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP, PORT))
    server_socket.listen()

    while True:
        conn, addr = server_socket.accept()

        client_thread = threading.Thread(target=client_connected, args=(conn,), daemon=True)
        client_thread.start()
