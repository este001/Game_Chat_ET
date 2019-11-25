import socket
from appJar import gui
import threading
import time
import tic_tac_toe as ttt
import sys

"""Client for game/chat application"""


def reset_challenger_buttons():
    """Resents all challenge related buttons to default"""

    app.setLabel('challenger_name', '')
    app.setButtonFg('Accept', 'Black')
    app.setButtonFg('Decline', 'Black')
    app.setLabelFg('challengelabel', 'darkgray')

    app.disableButton('Accept')
    app.disableButton('Decline')
    app.enableButton('CHALLENGE')


def strip_header(message):
    """Returns the message striped of it's header"""

    message = message[1:]
    return message


def font_colour_flashing(label_name, times):
    """Changes font-colour on selected label"""

    for i in range(times):
        app.setLabelFg(label_name, 'Red')
        time.sleep(1.5)
        app.setLabelFg(label_name, 'linen')
        time.sleep(0.5)
        app.setLabelFg(label_name, 'Red')


def game_challenge_countdown(label_name):
    """Counts down the challenge time"""

    global challenge_answer

    for i in range(5):
        if opponent in online_users:
            font_colour_flashing(label_name, 1)
            if i == 4 and not challenge_answer:
                reset_challenger_buttons()
                decline_challenge_button()

        else:
            app.setTextArea('Display', f'<<< {opponent} left the game >>>\n\n')
            reset_challenger_buttons()
            client_socket.sendall('R'.encode('utf-8'))
            break

    challenge_answer = False


def main_window_initiation():
    """Prepares and initiates the chat window"""

    create_game_gui()
    app.hideSubWindow('NameSubWindow')
    app.setTitle(f"ChatGameTE - {user_name}")
    app.disableEnter()
    app.enableEnter(send_message_button)
    app.show()

    receive_messages = threading.Thread(target=receive_from_server, daemon=True)
    receive_messages.start()


def confirm_exit():
    """Confirms if user really wants to quit"""

    if app.yesNoBox("Confirm Exit", "Are you sure you want to exit the application?"):
        client_socket.sendall("Q".encode('utf-8'))
        client_socket.close()
        return True
    else:
        return False


def confirm_exit_name_window():
    """Workaround function to close application properly in name sub window"""

    sys.exit()


# GAME FUNCTIONS
def enable_accept_decline_buttons():
    """Enables choice buttons when challenged"""

    app.enableButton('Accept')
    app.enableButton('Decline')
    app.setLabel('challenger_name', opponent)
    app.setButtonFg('Accept', 'Red')
    app.setButtonFg('Decline', 'Red')
    app.setLabelFg('challengelabel', 'Red')
    app.disableButton("CHALLENGE")


def start_game():
    """Creates an empty game_board"""

    game_board = ttt.start_game()
    return game_board


def check_game_state(player, next_player):
    """Checks every game move for win/tie/continue"""

    global game_turn
    global board

    if ttt.check_win_condition(board, player_dict_symbol[player]):
        app.setLabel('winner_name', player)
        disable_all_game_buttons()
        colour_thread = threading.Thread(target=font_colour_flashing, args=('winner_name', 3), daemon=True)
        colour_thread.start()
    elif ttt.tie(board):
        app.setLabel('winner_name', '--TIE--')
        disable_all_game_buttons()
    else:
        app.setLabel('player_turn_name', next_player)
        if next_player == user_name:
            game_turn = True
        else:
            game_turn = False


def place_player_mark(player, game_board, coordinates, player_dict_symbol):
    """Places players symbols in backend game"""

    game_board = ttt.user_input(coordinates, game_board, player_dict_symbol[player])
    return game_board


def disable_all_game_buttons():
    """Disables all buttons on game board"""

    app.disableButton('00')
    app.disableButton('01')
    app.disableButton('02')
    app.disableButton('10')
    app.disableButton('11')
    app.disableButton('12')
    app.disableButton('20')
    app.disableButton('21')
    app.disableButton('22')


def default_board():
    """Resets the game board window to default"""

    global board

    board = ttt.start_game()
    app.setButtonImage("00", "game_empty.gif")
    app.setButtonImage("01", "game_empty.gif")
    app.setButtonImage("02", "game_empty.gif")
    app.setButtonImage("10", "game_empty.gif")
    app.setButtonImage("11", "game_empty.gif")
    app.setButtonImage("12", "game_empty.gif")
    app.setButtonImage("20", "game_empty.gif")
    app.setButtonImage("21", "game_empty.gif")
    app.setButtonImage("22", "game_empty.gif")

    app.setLabel('winner_name', '')

    app.enableButton('00')
    app.enableButton('01')
    app.enableButton('02')
    app.enableButton('10')
    app.enableButton('11')
    app.enableButton('12')
    app.enableButton('20')
    app.enableButton('21')
    app.enableButton('22')


def confirm_quit_game():
    """Confirms if players want to exit, then resets the board"""

    if app.yesNoBox("Confirm Exit", "Are you sure you want to exit the game?"):
        client_socket.sendall("R".encode('utf-8'))
        app.enableButton("CHALLENGE")
        default_board()
        app.hideSubWindow(f"GameWindow - {user_name}")
        return True
    else:
        return False


# RECEIVE
def receive_broadcast(incoming_message):
    """Displays incoming broadcast messages"""

    message = strip_header(incoming_message)
    app.setTextArea('Display', message + '\n\n')


def receive_online_users(incoming_message):
    """Updates the online users list"""

    global online_users

    names = incoming_message.lstrip("O")
    users_online = names.split('-')
    users_online.pop()

    online_users = users_online

    app.clearListBox('Online_users_listbox')
    app.addListItems('Online_users_listbox', users_online)


def receive_game_turn(incoming_message):
    """Handles opponents game move"""

    global board

    coordinates = incoming_message[1:3]
    board = place_player_mark(opponent, board, coordinates, player_dict_symbol)
    app.setButtonImage(coordinates, player_dict[opponent])
    app.disableButton(coordinates)
    check_game_state(opponent, user_name)


def receive_challenge(incoming_message):
    """Handles a challenge from challenger"""

    global opponent
    opponent = incoming_message[1:]

    challenge_message = f"<<< {opponent} has challenged you >>>\n\n"
    app.setTextArea('Display', challenge_message)
    enable_accept_decline_buttons()

    colour_thread = threading.Thread(target=game_challenge_countdown, args=('challenger_name',), daemon=True)
    colour_thread.start()


def receive_accepted_challenge(incoming_message):
    """Initiates a game when challenge is accepted"""

    global player_dict
    global player_dict_symbol
    global game_turn
    global opponent_answer

    game_turn = True
    opponent_answer = True

    message = strip_header(incoming_message)
    app.setTextArea('Display', f"<<< {message} >>>\n\n")
    app.setLabel('Player1', user_name)
    app.setLabel('Player2', opponent)
    app.setLabel('player_turn_name', user_name)
    player_dict = {user_name: 'game_cross.gif',
                   opponent: 'game_circle.gif'}
    player_dict_symbol = {user_name: 'x',
                          opponent: 'o'}

    app.showSubWindow(f"GameWindow - {user_name}", hide=False)


def receive_declined_challenge(incoming_message):
    """Prints challenge decline message to challenger"""

    global opponent_answer
    opponent_answer = True

    message = strip_header(incoming_message)

    app.setTextArea('Display', f'<<< {message} >>>\n\n')
    app.enableButton('CHALLENGE')


def receive_from_server():
    """Directs message depending on message header"""

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
        app.disableEnter(),


# BUTTONS
def send_message_button():
    """Function sends broadcast message to server"""

    my_message = app.getTextArea('Message_entry')
    if len(my_message) > 0:
        my_message = f"S{my_message}".encode('utf-8')
        client_socket.sendall(my_message)
        app.clearTextArea('Message_entry')


def name_submit_button():
    """Initiates main window when name is valid"""

    global user_name

    user_name = app.getEntry('NameEntry')
    if 0 < len(user_name) <= 10:
        message = f"N{user_name}".encode('utf-8')
        client_socket.sendall(message)
        name_validation = bool(int(client_socket.recv(1024).decode('utf-8')))

        if not name_validation:
            main_window_initiation()
        else:
            app.errorBox('Invalid name', 'Name is not available\nPlease try another one.')
            app.clearEntry('NameEntry')
    else:
        app.errorBox('Invalid name', 'Name needs to be 1-10 characters')


def cancel_button():
    """Closes window"""

    app.stop()


def quit_game():
    """Handles a game quit"""

    global board

    client_socket.sendall("R".encode('utf-8'))
    app.enableButton("CHALLENGE")
    default_board()
    board = ttt.start_game()
    app.hideSubWindow(f"GameWindow - {user_name}")


def accept_challenge_button():
    """Initiates a game when accepted a challenge"""

    global player_dict
    global player_dict_symbol
    global game_turn
    global challenge_answer

    game_turn = False
    challenge_answer = True
    reset_challenger_buttons()
    app.setLabel('Player1', opponent)
    app.setLabel('Player2', user_name)
    app.setLabel('player_turn_name', opponent)

    player_dict = {opponent: 'game_cross.gif',
                   user_name: 'game_circle.gif'}
    player_dict_symbol = {opponent: 'x',
                          user_name: 'o'}

    accept_message = f"A{opponent}".encode('utf-8')
    client_socket.sendall(accept_message)

    app.showSubWindow(f"GameWindow - {user_name}", hide=False)


def decline_challenge_button():
    """Sends a decline message to server"""
    global challenge_answer
    challenge_answer = True

    reset_challenger_buttons()
    client_socket.sendall(f"D{opponent}".encode('utf-8'))


def challenge_player_thread():

    global opponent_answer

    while not opponent_answer:
        if opponent not in online_users:
            reset_challenger_buttons()
            client_socket.sendall('R'.encode('utf-8'))
            break
    opponent_answer = False


def challenge_player_button():
    """Challenge selected player"""

    global opponent

    try:
        opponent = app.getListBox('Online_users_listbox')[0]

        if opponent != user_name:
            challenge = f"C{opponent}".encode('utf-8')
            client_socket.sendall(challenge)
            app.disableButton("CHALLENGE")

            challenge_thread = threading.Thread(target=challenge_player_thread, daemon=True)
            challenge_thread.start()
        else:
            app.setTextArea('Display', "<<< You can't challenge yourself >>>\n\n")
    except IndexError:
        app.setTextArea('Display', '<<< Select a player to challenge >>> \n\n')


def game_button(button_name):
    """Sends the game-button name to server"""

    global game_turn
    global board

    if game_turn:
        board = place_player_mark(user_name, board, button_name, player_dict_symbol)
        app.setButtonImage(button_name, player_dict[user_name])
        app.disableButton(button_name)
        message = f"G{button_name}{opponent}".encode('utf-8')
        client_socket.sendall(message)
        check_game_state(user_name, opponent)


def buttons(name):
    """Directs pressed button to right function"""

    button_dict = {'Submit': name_submit_button,
                   'Cancel': cancel_button,
                   'Send': send_message_button,
                   'Close': cancel_button,
                   'Accept': accept_challenge_button,
                   'Decline': decline_challenge_button,
                   'CHALLENGE': challenge_player_button,
                   'Quit game': quit_game}

    for k, v in button_dict.items():
        if k == name:
            v()


# GUI
def create_game_gui():
    """Creates the gui for game board"""

    # GAME SUB WINDOW
    app.startSubWindow(f'GameWindow - {user_name}')
    app.setResizable(canResize=False)
    app.setStopFunction(confirm_quit_game)
    app.addLabel('lefttopfiller', ' ', 0, 0)
    app.addLabel('righttopfiller', ' ', 0, 2)
    app.startLabelFrame('Tic Tac Toe', 0, 1)

    app.addEmptyLabel('emptyLabel1')
    app.setPadding(3, 8)
    app.setSticky('n')
    app.addLabel('Player1', 'Player 1', 1, 0)
    app.getLabelWidget('Player1').config(font="Verdana 13 bold")
    app.setLabelFg('Player1', 'mediumblue')

    app.setSticky('n')
    app.addLabel('vs', 'VS.', 1, 1)
    app.setSticky('n')
    app.addLabel('Player2', 'Player 2', 1, 2)
    app.getLabelWidget('Player2').config(font="Verdana 13 bold")
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
    app.getLabelWidget('winner').config(font="Verdana 11 bold")
    app.getLabelWidget('winner_name').config(font="Verdana 11 bold")

    app.setSticky('s')
    app.addButton('Quit game', buttons, 7, 2)
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
    app.setStopFunction(confirm_exit_name_window)
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

    # Challange buttons
    app.addButton('CHALLENGE', buttons, 0, 1, colspan=3)
    app.addLabel('challengelabel', 'Challenged by:', 1, 1, colspan=3)
    app.setLabelFg('challengelabel', 'darkgray')
    app.getLabelWidget('challengelabel').config(font="verdana 11 bold")
    app.addLabel('challenger_name', '', 2, 1, colspan=3)
    app.getLabelWidget('challenger_name').config(font="verdana 14 bold")

    app.addButton('Accept', buttons, 3, 1)
    app.addButton('Decline', buttons, 3, 3)
    app.disableButton('Accept')
    app.disableButton('Decline')

    # Chat buttons
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
    ta1.config(font="Verdana 10 bold")
    ta2.config(font="Verdana 10 bold")
    app.setStopFunction(confirm_exit)


if __name__ == '__main__':

    online_users = []
    board = start_game()
    user_name = ''
    opponent = ''
    game_turn = False
    game_finished = False
    opponent_answer = False
    challenge_answer = False
    player_dict = {}
    player_dict_symbol = {}

    IP = "127.0.0.1"
    PORT = 1234

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((IP, PORT))

    app = gui("ChatGameTE")
    create_gui()
    app.go(startWindow='NameSubWindow')
