import socket
from appJar import gui
import threading

"""Client for game/chat application"""




def receive_from_server(client_socket):
    while True:
        pass



def name_submit_button():

    name = app.getEntry('NameEntry')
    if len(name) != 0:
        client_socket.sendall(name.encode('utf-8'))
        name_validation = bool(int(client_socket.recv(1024).decode('utf-8')))

        if not name_validation:
            receive_messages = threading.Thread(target=receive_from_server, args=(client_socket,))
            receive_messages.start()

            app.destroyAllSubWindows()
            app.show()
        else:
            app.errorBox('Invalid name', 'Name is not available\nPlease try another one.')
            app.clearEntry('NameEntry')
    else:
        app.errorBox('Invalid name', 'Name needs to contain at least one character')

# TODO Fix this function
def exit_button():
    client_socket.sendall(''.encode('utf-8'))


def buttons(name):

    button_dict = {'Submit': name_submit_button,
                   'Exit': exit_button}

    for k, v in button_dict.items():
        if k == name:
            v()

# TODO Create main window and game subwindow + style
def create_gui():

    # NAME SUBWINDOW
    app.startSubWindow('NameSubWindow', modal=True)
    app.startLabelFrame('Login')
    app.setSize("280x135")

    app.addLabel('L1', 'Enter username', 0, 0)
    app.addEntry('NameEntry', 1, 0)
    app.addButtons(['Submit', 'Exit'], buttons, 2, 0)

    app.stopLabelFrame()
    app.stopSubWindow()

    # MAIN WINDOW
    app.setSize('650x400')
    app.setResizable(canResize=False)
    app.startFrame('OuterFRAME', 1, 0)
    app.startLabelFrame('')

    # Makes a column of empty labels to the left
    for i in range(8):
        if i == 7:
            i += 1
        app.addEmptyLabel('Label' + str(i), i, 0)

    # DISPLAY
    app.addScrolledTextArea('Display', 0, 1, 6, 6)
    app.disableTextArea('Display')
    app.setTextAreaHeight('Display', 20)
    app.setTextAreaWidth('Display', 55)

    # PLAYERS ONLINE LIST
    app.addTextArea('online_display', 0, 7, rowspan=6)
    app.disableTextArea('online_display')

    # ENTRY AREA
    app.addTextArea('usersText', 7, 1, 6)
    app.setTextAreaHeight('usersText', 5)
    app.setTextAreaWidth('usersText', 60)

    # BUTTONS
    app.startFrame('buttonFrame', 7, 7, rowspan=5)

    app.setPadding([2, 30])
    app.addLabel('bl1', ' ', 3, 0)
    app.addLabel('bl2', ' ', 3, 4)

    app.addButton('Send', buttons, 3, 1)
    app.addLabel('filler', ' ', 3, 2)
    app.addButton('Close', buttons, 3, 3)

    app.stopFrame()  # buttonFrame
    app.stopLabelFrame()
    app.stopFrame()  # OuterFRAME

    app.setFont(size=10, family='Verdana', weight='bold')
    ta1 = app.getTextAreaWidget("usersText")
    ta2 = app.getTextAreaWidget("Display")
    ta1.config(font=("Verdana 10 bold"))
    ta2.config(font=("Verdana 10 bold"))


if __name__ == '__main__':

    IP = "127.0.0.1"
    PORT = 1234

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((IP, PORT))

    app = gui()
    create_gui()
    app.go(startWindow='NameSubWindow')
