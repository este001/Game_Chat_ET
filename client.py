import socket
from appJar import gui

"""Client for game/chat application"""

def button(name):

    if name == 'Submit':
        pass
    elif name == 'Exit':
        pass


def create_gui():

    app = gui()

    # NAME SUBWINDOW
    app.startSubWindow('NameSubWindow', modal=True)
    app.startLabelFrame('Login')

    app.addLabel('L1', 'Enter username', 0, 0)
    app.addEntry('NameEntry', 1, 0)
    app.addButtons(['Submit', 'Exit'], button, 2, 0)

    app.stopLabelFrame()
    app.stopSubWindow()

    # MAIN WINDOW

    # GAME SUBWINDOW

if __name__ == '__main__':

    IP = "127.0.0.1"
    PORT = 1234

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((IP, PORT))


    while True:
        name = input('Name: ')
        client_socket.sendall(name.encode('utf-8'))
        name_validation = bool(int(client_socket.recv(1024).decode('utf-8')))

        if not name_validation:
            print('Namnet godkänt!')

        else:
            print('Namnet är upptaget!')


    create_gui()
    app.go(startWindow='NameSubWindow')