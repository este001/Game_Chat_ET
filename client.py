import socket
import appJar

"""Client for game/chat application"""


if __name__ == '__main__':

    IP = "127.0.0.1"
    PORT = 1234

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((IP, PORT))

    while True:
        name = input('Name: ')
        client_socket.sendall(name.encode('utf-8'))
        name_validation = bool(int(client_socket.recv(1024).decode('utf-8')))

        if name_validation:
            print('Namnet är upptaget!')

        print('Namnet godkänt!')


