"""
TIC TAC TOE
Game logic
"""


def horizontal_win_condition(board):
    if board[0][0:4] == ['x', 'x', 'x']:
        return True
    elif board[1][0:4] == ['x', 'x', 'x']:
        return True
    elif board[2][0:4] == ['x', 'x', 'x']:
        return True
    else:
        return False


def vertical_win_condition():
    pass


def diagonal_win_condition():
    pass


def check_win_condition():
    # if horizontal() or vertical() or diagonal():
    pass


def user_input(coordinate, board, player_input):
    board[coordinate[0]].pop(coordinate[1])
    board[coordinate[0]].insert(coordinate[1], player_input)
    return board


def start_game():
    game_board = [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]
    return game_board


if __name__ == '__main__':
    start_game()
