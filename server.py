import socket
import threading
import time
import tic_tac_toe as ttt


def Game(player1, player2):
    try:
        board = ttt.start_game()
        symbol = {player1: 'x', player2: 'o'}
        while True:
            game_message = player1.recv(1024)
            game_message = game_message.decode('utf-8')
            if game_message[0] == "G":
                print("DET ÄR ETT G")
            coordinate = (int(game_message[1:2]), int(game_message[2:3]))

            #ttt.user_input(coordinate,board, symbol[game_message[]] )
            if ttt.check_win_condition(board, game_message[1:3]):
                # rec G22Tim/Este
                break

    except Exception as e:
        print(e)


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


def player_accepted_challenge(clients, player1, player2):
    player1 = player1.decode('utf-8')
    for c in clients:
        if clients[c] == player1:
            c.sendall(f"A{clients[c]} has accepted {clients[player2]} challenge".encode('utf-8'))


def player_declined_challenge(clients, name, conn):
    challenger = name[1:]
    challenger = challenger.decode('utf-8')
    player_game_status[clients[conn]] = True
    player_game_status[challenger] = True
    message = f"D{clients[conn]} has declined a challenge from {challenger}"
    for c in clients:
        if clients[c] == challenger:
            c.sendall(message.encode('utf-8'))
            conn.sendall(message.encode('utf-8'))


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

    player_game_status[player_to_challenge] = False
    for c in clients:
        if clients[c] == player_to_challenge:
            c.sendall(f'C{challenger}'.encode('utf-8'))


def whisper_message(whispered_message, clients, conn):
    whispered_message = whispered_message[1:]
    user_to_whisper_list = whispered_message.split()
    user_to_whisper_list = [user.strip('@') for user in user_to_whisper_list if user[0] == '@']
    for c in clients:
        if [True for user in user_to_whisper_list if clients[c] == user]:
            c.sendall(f'S{clients[conn]} whispered > {whispered_message}'.encode('utf-8'))
    conn.sendall(f'S{clients[conn]} whispered > {whispered_message}'.encode('utf-8'))


def receive_messages(conn):
    try:
        while True:
            message = conn.recv(1024)
            if not message:
                break

            elif '@' in message.decode('utf-8'):
                whisper_message(message.decode('utf-8'), clients, conn)

            elif message[0:1].decode('utf-8') == "S":
                broadcast_message(message, clients, conn)

            elif message[0:1].decode('utf-8') == "C":
                if player_availability(message[1:].decode('utf-8')):
                    game_challenge(conn, message, clients)
                else:
                    conn.sendall(f'DPlayer is unavailable'.encode('utf-8'))
            elif message[0:1].decode('utf-8') == "A":
                player_accepted_challenge(clients, message[1:], conn)
                game_thread = threading.Thread(target=Game, args=(clients[conn], message[1:]), daemon=True)
                game_thread.start()

            elif message[0:1].decode('utf-8') == "D":
                player_declined_challenge(clients, message, conn)

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
