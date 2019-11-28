import socket
import threading
import time


def strip_header(message):
    """Returns the message striped of it's header"""

    message = message[1:]
    return message


def whisper_message(whispered_message, clients, conn):
    """Sends direct message to all users with an @ sign"""

    whispered_message = strip_header(whispered_message)
    user_to_whisper_list = whispered_message.split()
    user_to_whisper_list = [user.strip('@') for user in user_to_whisper_list if user[0] == '@']
    for c in clients:
        if [True for user in user_to_whisper_list if clients[c] == user]:
            c.sendall(f'S{clients[conn]} whispered > {whispered_message}'.encode('utf-8'))
    conn.sendall(f'S{clients[conn]} whispered > {whispered_message}'.encode('utf-8'))


def send_message(message, clients):
    """Sends message to all users ex. Tim has connected and sends list of users online"""

    for c in clients:
        c.sendall(message.encode('utf-8'))


def username_exists(user_name, clients):
    """Checks if username exists in clients dict"""

    if user_name in clients.values():
        return True
    else:
        return False


def broadcast_message(message, clients, conn):
    """ Broadcasts message to all users """

    user = clients[conn]
    message = f"S{user} > {message[1:]}".encode('utf-8')
    for c in clients:
        c.sendall(message)


def player_accepted_challenge(clients, player1, player2):
    """ Returns an accept message to the challenger """

    for c in clients:
        if clients[c] == player1:
            c.sendall(f"A{clients[c]} has accepted {clients[player2]} challenge".encode('utf-8'))


def player_declined_challenge(clients, name, conn):
    """ Returns a decline message to the challenger"""

    challenger = strip_header(name)
    player_game_status[clients[conn]] = True
    player_game_status[challenger] = True
    message = f"D{clients[conn]} has declined a challenge from {challenger}"
    for c in clients:
        if clients[c] == challenger:
            c.sendall(message.encode('utf-8'))
            conn.sendall(message.encode('utf-8'))


def reset_player_availability(conn, clients):
    """ Resets user availability """

    player_game_status[clients[conn]] = True
    return True


def player_availability(player):
    """ Returns true or false if player is available"""

    if player_game_status[player]:
        return True
    else:
        return False


def game_challenge(conn, message, clients):
    """ Sends a challenge message to a user """

    challenger = clients[conn]
    player_game_status[clients[conn]] = False
    player_to_challenge = strip_header(message)

    player_game_status[player_to_challenge] = False
    for c in clients:
        if clients[c] == player_to_challenge:
            c.sendall(f'C{challenger}'.encode('utf-8'))


def game_turn_coordinates(message):
    """ Sends coordinats to players """

    receiver = message[3:]
    game_move = message[1:3]
    for c in clients:
        if clients[c] == receiver:
            message = f"G{game_move}{clients[conn]}"
            c.sendall(message.encode('utf-8'))


def receive_messages(conn):
    try:
        while True:
            message = conn.recv(1024)
            message = message.decode('utf-8')
            # Quit header
            if message[0] == "Q":
                break
            # Whisper header
            elif '@' in message:
                whisper_message(message, clients, conn)

            # Broadcast header
            elif message[0:1] == "S":
                broadcast_message(message, clients, conn)

            # Challenge header
            elif message[0:1] == "C":
                if player_availability(message[1:]):
                    game_challenge(conn, message, clients)
                else:
                    conn.sendall(f'DPlayer is unavailable'.encode('utf-8'))

            # Accept challenge header
            elif message[0:1] == "A":
                player_accepted_challenge(clients, message[1:], conn)

            # Game coordiantes header
            elif message[0:1] == "G":
                game_turn_coordinates(message)

            # Decline header
            elif message[0:1] == "D":
                player_declined_challenge(clients, message, conn)

            # Reset player status header
            elif message[0:1] == "R":
                reset_player_availability(conn, clients)

        print(f"{clients[conn]} has disconnected")

        conn.close()
        del clients[conn]
        send_message(online_users(clients), clients)

    except ConnectionResetError as cre:
        print('receive message', cre)
        send_message(f"S<{clients[conn]} has disconnected >", clients)
        conn.close()
        del clients[conn]
        send_message(online_users(clients), clients)


def online_users(clients):
    users_online = "O"
    for c in clients:
        users_online += clients[c] + '-'
    return users_online


def client_connected(conn):
    try:
        while True:
            user_name = conn.recv(1024)
            user_name = strip_header(user_name.decode('utf-8'))

            if user_name[0] == "Q":
                break

            if username_exists(user_name[1:], clients):
                conn.sendall('1'.encode('utf-8'))

            else:
                conn.sendall('0'.encode('utf-8'))
                clients[conn] = user_name
                player_game_status[user_name] = True
                broadcast_message(message="Shas connected", conn=conn, clients=clients)
                time.sleep(1)
                send_message(online_users(clients), clients)
                receive_messages(conn)
                break
        conn.close()
    except ConnectionResetError as e:

        print("client_connected - ", e)
        conn.close()
        del clients[conn]


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
