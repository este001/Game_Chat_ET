import socket
from appJar import gui
import threading
import time

"""Client for game/chat application"""


def reset_challenger_buttons():
    """Resents all challenge related buttons to default"""

    app.setLabel('challenger_name', '')
    app.setButtonFg('Accept', 'Black')
    app.setButtonFg('Decline', 'Black')
    app.setLabelFg('challengelabel', 'darkgray')
    app.disableButton('Accept')
    app.disableButton('Decline')


def strip_header(message):
    """Returns the message striped of it's header"""

    message = message[1:]
    return message


def challenger_colour_change():
    """Sets challenger name and buttons to flashing-mode"""

    while True:
        app.setLabelFg('challenger_name', 'Red')
        time.sleep(1.50)
        app.setLabelFg('challenger_name', 'linen')
        time.sleep(0.5)


# RECEIVE
def receive_broadcast(incoming_message):
    """Displays incoming broadcast messages"""

    message = strip_header(incoming_message)
    app.setTextArea('Display', message + '\n\n')


def receive_online_users(incoming_message):
    names = incoming_message.lstrip("O")
    users_online = names.split('-')
    users_online.pop()

    app.clearListBox('Online_users_listbox')
    app.addListItems('Online_users_listbox', users_online)


# TODO
def receive_game_turn(incoming_message):

    global game_turn

    game_move = incoming_message[1:3]
    player = incoming_message[3:]
    app.setButtonImage(game_move, player_dict[player])
    app.setLabel('player_turn_name', user_name)
    game_turn = True


def receive_challenge(incoming_message):

    global challenger_name
    challenger_name = incoming_message[1:]

    challenge_message = f"<<< {incoming_message[1:]} has challenged you >>>\n\n"
    app.setTextArea('Display', challenge_message)

    app.enableButton('Accept')
    app.enableButton('Decline')
    app.setLabel('challenger_name', incoming_message[1:])

    app.setButtonFg('Accept', 'Red')
    app.setButtonFg('Decline', 'Red')
    app.setLabelFg('challengelabel', 'Red')
    app.disableButton("CHALLENGE")

    # TODO Fix this
    colour_thread = threading.Thread(target=challenger_colour_change, daemon=True)
    colour_thread.start()


def receive_accepted_challenge(incoming_message):

    global opponent
    global player_dict
    global game_turn
    game_turn = True

    opponent = challenged_player
    message = strip_header(incoming_message)
    app.setTextArea('Display', f"<<< {message} >>>")
    app.setLabel('Player1', user_name)
    app.setLabel('Player2', opponent)
    app.setLabel('player_turn_name', user_name)
    player_dict = {user_name: 'game_cross.gif',
                   opponent: 'game_circle.gif'}


    app.showSubWindow(f"GameWindow - {user_name}", hide=False)


def receive_declined_challenge(incoming_message):
    """Prints message to challenger"""

    message = strip_header(incoming_message)

    app.setTextArea('Display', f'<<< {message} >>>\n\n')
    app.enableButton('CHALLENGE')


def receive_from_server():
    try:
        while True:
            incoming_message = client_socket.recv(1024)
            if not incoming_message:
                break
            incoming_message = incoming_message.decode('utf-8')
            if incoming_message[0:1] == "S":
                receive_broadcast(incoming_message)
            elif incoming_message[0:1] == "C":
                receive_challenge(incoming_message)
            elif incoming_message[0:1] == "O":
                receive_online_users(incoming_message)
            elif incoming_message[0:1] == "G":
                receive_game_turn(incoming_message)
            elif incoming_message[0:1] == "A":
                receive_accepted_challenge(incoming_message)
            elif incoming_message[0:1] == "D":
                receive_declined_challenge(incoming_message)



    except (ConnectionAbortedError, ConnectionResetError) as error:
        print('Receive_from_server error: ', error)
        app.setTextArea('Display', '---LOST CONNECTION TO SERVER---')
        app.disableButton('CHALLENGE')
        app.disableButton('Send')
        app.disableButton('Accept')
        app.disableButton('Decline')
        app.disableEnter()


# BUTTONS
def send_message_button():

    my_message = app.getTextArea('Message_entry')
    if len(my_message) > 0:
        my_message = f"S{my_message}".encode('utf-8')
        client_socket.sendall(my_message)
        app.clearTextArea('Message_entry')


def name_submit_button():

    global user_name

    name = app.getEntry('NameEntry')
    if len(name) != 0:
        client_socket.sendall(name.encode('utf-8'))
        name_validation = bool(int(client_socket.recv(1024).decode('utf-8')))

        if not name_validation:
            app.destroySubWindow('NameSubWindow')
            app.setTitle(f"ChatGameTE - {name}")
            app.show()
            app.disableEnter()
            user_name = name
            app.enableEnter(send_message_button)
            create_game_gui()
            receive_messages = threading.Thread(target=receive_from_server, daemon=True)
            receive_messages.start()

        else:
            app.errorBox('Invalid name', 'Name is not available\nPlease try another one.')
            app.clearEntry('NameEntry')
    else:
        app.errorBox('Invalid name', 'Name needs to contain at least one character')


def cancel_button():
    client_socket.close()
    app.stop()


def accept_challenge_button():

    global opponent
    global player_dict
    global game_turn
    game_turn = False

    opponent = challenger_name
    reset_challenger_buttons()
    app.setLabel('Player1', opponent)
    app.setLabel('Player2', user_name)
    app.setLabel('player_turn_name', challenger_name)

    player_dict = {challenger_name: 'game_cross.gif',
                   user_name: 'game_circle.gif'}

    accept_message = f"A{challenger_name}".encode('utf-8')
    client_socket.sendall(accept_message)


    app.showSubWindow(f"GameWindow - {user_name}", hide=False)


def decline_challenge_button():
    """Sends a decline message to server"""

    reset_challenger_buttons()
    client_socket.sendall(f"D{challenger_name}".encode('utf-8'))


def challenge_player_button():
    """Challenge selected player"""

    global challenged_player

    challenged_player = app.getListBox('Online_users_listbox')[0]

    if challenged_player != user_name:
        challenge = f"C{challenged_player}".encode('utf-8')
        client_socket.sendall(challenge)
        app.disableButton("CHALLENGE")


def game_button(button_name):
    """Sends the game-button name to server"""

    global game_turn

    if game_turn:
        message = f"G{button_name}{user_name}".encode('utf-8')
        client_socket.sendall(message)
        app.setLabel('player_turn_name', opponent)
        game_turn = False


def buttons(name):
    """Directs pressed button to right function"""

    button_dict = {'Submit': name_submit_button,
                   'Cancel': cancel_button,
                   'Send': send_message_button,
                   'Close': cancel_button,
                   'Accept': accept_challenge_button,
                   'Decline': decline_challenge_button,
                   'CHALLENGE': challenge_player_button}

    for k, v in button_dict.items():
        if k == name:
            v()


def create_game_gui():

    # GAME SUB WINDOW
    app.startSubWindow(f'GameWindow - {user_name}')
    app.addLabel('lefttopfiller', ' ', 0, 0)
    app.addLabel('righttopfiller', ' ', 0, 2)
    app.startLabelFrame('Tic Tac Toe', 0, 1)

    app.addEmptyLabel('emptyLabel1')
    app.setPadding(3,8)
    app.setSticky('w')
    app.addLabel('Player1', 'Player 1', 1, 0)
    app.setLabelFg('Player1', 'mediumblue')
    app.setSticky('n')
    app.addLabel('vs', 'VS.', 1, 1)
    app.setSticky('e')
    app.addLabel('Player2', 'Player 2', 1, 2)
    app.setLabelFg('Player2', 'red')
    app.addEmptyLabel('emptyLabel2')

    # Game buttons
    app.startFrame('gamebuttonframe', 2, 0, colspan=3, rowspan=3)
    app.addImageButton("00", game_button, "game_empty.gif", 0, 0)
    app.addImageButton("01", game_button, "game_empty.gif", 0, 1)
    app.addImageButton("02", game_button, "game_empty.gif", 0, 2)
    app.addImageButton("10", game_button, "game_empty.gif", 1, 0)
    app.addImageButton("11", game_button, "game_empty.gif", 1, 1)
    app.addImageButton("12", game_button, "game_empty.gif", 1, 2)
    app.addImageButton("20", game_button, "game_empty.gif", 2, 0)
    app.addImageButton("21", game_button, "game_empty.gif", 2, 1)
    app.addImageButton("22", game_button, "game_empty.gif", 2, 2)

    app.stopFrame()
    app.setSticky('w')
    app.setPadding(3, 10)
    app.addLabel('player_turn', f"Player's turn:", 5, 0)
    app.addLabel('player_turn_name', '', 5, 1, colspan=2)
    app.addLabel('winner', 'Winner: ', 6, 0)
    app.addLabel('winner_name', '', 6, 1, colspan=2)
    app.getLabelWidget('winner').config(font=("Verdana 11 bold"))
    app.getLabelWidget('winner_name').config(font=("Verdana 11 bold"))

    app.setSticky('s')
    app.addButton('Quit game', buttons,7, 2)
    app.stopLabelFrame()
    app.stopSubWindow()


def create_gui():
    """Creates the gui for the application"""

    # SUBWINDOW LOGIN
    app.startSubWindow("NameSubWindow", modal=True)
    app.enableEnter(name_submit_button)
    app.setSize("280x135")
    app.setResizable(canResize=False)
    app.startLabelFrame('ChatGame', 1, 0)

    app.setPadding([5, 0])
    app.addLabel('leftfiller', '        ', 0, 0)
    app.addLabel('rightfiller', '        ', 0, 2)

    app.startFrame('functionality', 0, 1)

    app.addLabel("usernamelabel", "- Enter Username -", 0, 0, colspan=2)
    app.getLabelWidget("usernamelabel").config(font="verdana 11 bold")
    app.addEntry('NameEntry', 1, 0, colspan=2)
    app.setFocus('NameEntry')
    app.setEntryAnchor('NameEntry', 'center')

    # Subwindow Button
    app.startFrame('buttonframe', 2, 0)
    app.setPadding([0, 15])
    app.setSticky('')
    app.addButton('Submit', buttons, 2, 0)
    app.addLabel('buttonfiller', '', 2, 1)
    app.addButton('Cancel', buttons, 2, 2)
    app.stopFrame()

    app.stopFrame()  # functionality
    app.stopLabelFrame()
    app.stopSubWindow()


    # MAIN WINDOW
    app.setSize('750x400')
    app.setResizable(canResize=False)

    app.startFrame('Outer_frame', 1, 0)
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
    app.setTextAreaWidth('Display', 60)

    # PLAYERS ONLINE LIST
    app.addListBox('Online_users_listbox', online_users, 0, 7, rowspan=4)

    # MESSAGE ENTRY
    app.addTextArea('Message_entry', 7, 1, 6)
    app.setTextAreaHeight('Message_entry', 6)
    app.setTextAreaWidth('Message_entry', 60)

    # BUTTONS
    app.startFrame('button_frame', 4, 7, rowspan=5)
    app.setPadding([1, 8])
    app.addLabel('bl1', ' ', 1, 0)
    app.addLabel('bl2', ' ', 1, 4)

    #Challange buttons
    app.addButton('CHALLENGE', buttons, 0, 1, colspan=3)
    app.addLabel('challengelabel', 'Challenged by:', 1, 1, colspan=3)
    app.setLabelFg('challengelabel', 'darkgray')                        # Turns red when challanged
    app.getLabelWidget('challengelabel').config(font="verdana 11 bold")
    app.addLabel('challenger_name', '', 2, 1, colspan=3)                # Challengers name goes in here when challanged
    app.getLabelWidget('challenger_name').config(font="verdana 14 bold")

    app.addButton('Accept', buttons, 3, 1)
    app.addButton('Decline', buttons, 3, 3)
    app.disableButton('Accept')
    app.disableButton('Decline')

    #Chat buttons
    app.addButton('Send', buttons, 4, 1)
    app.addLabel('filler', '', 4, 2)
    app.addButton('Close', buttons, 4, 3)
    app.stopFrame()  # button_frame

    app.stopLabelFrame()
    app.stopFrame()  # Outer_frame


    # GENERAL DESIGN
    app.setFont(size=10, family='Verdana', weight='bold')
    ta1 = app.getTextAreaWidget("Message_entry")
    ta2 = app.getTextAreaWidget("Display")
    ta1.config(font=("Verdana 10 bold"))
    ta2.config(font=("Verdana 10 bold"))


if __name__ == '__main__':


    online_users = []

    user_name = ''
    opponent = ''
    challenger_name = ''
    challenged_player = ''
    game_turn = False
    game_finished = False
    player_dict = {}


    IP = "127.0.0.1"
    PORT = 1234

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((IP, PORT))

    app = gui("ChatGameTE")
    create_gui()
    app.go(startWindow='NameSubWindow')
