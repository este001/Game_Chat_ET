import socket
from appJar import gui

"""Client for game/chat application"""


def name_submit_button():

    name = app.getEntry('NameEntry')
    if len(name) != 0:
        client_socket.sendall(name.encode('utf-8'))
        name_validation = bool(int(client_socket.recv(1024).decode('utf-8')))

        if not name_validation:
            print('Namnet godkänt!')

        else:
            app.errorBox('Invalid name', 'Name is not available\nPlease try another one.')
            app.clearEntry('NameEntry')
    else:
        app.errorBox('Invalid name', 'Name needs to contain at least one character')


def exit_button():
    pass


def buttons(name):

    button_dict = {'Submit': name_submit_button,
                   'Exit': exit_button}

    for k, v in button_dict.items():
        if k == name:
            v()


def create_gui():

    # NAME SUBWINDOW
    app.startSubWindow('NameSubWindow', modal=True)
    app.setSize("280x135")
    app.startLabelFrame('Login')

    app.addLabel('L1', 'Enter username', 0, 0)
    app.addEntry('NameEntry', 1, 0)
    app.addButtons(['Submit', 'Exit'], buttons, 2, 0)

    app.stopLabelFrame()
    app.stopSubWindow()

    # MAIN WINDOW


    # GAME SUBWINDOW


if __name__ == '__main__':

    IP = "127.0.0.1"
    PORT = 1234

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((IP, PORT))

    app = gui()
    create_gui()
    app.go(startWindow='NameSubWindow')