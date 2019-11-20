"""
TIC TAC TOE
Game logic
ps = x
['x', 'o', 'x']   = ['ps', 'ps', 'ps']
"""


def horizontal_win_condition(board, player_symbol):
    if board[0][0:4] == [player_symbol, player_symbol, player_symbol]:
        return True
    elif board[1][0:4] == [player_symbol, player_symbol, player_symbol]:
        return True
    elif board[2][0:4] == [player_symbol, player_symbol, player_symbol]:
        return True
    else:
        return False


def vertical_win_condition(board, player_symbol):
    if board[0][0] == player_symbol and board[1][0] == player_symbol and board[2][0] == player_symbol:
        return True
    elif board[0][1] == player_symbol and board[1][1] == player_symbol and board[2][1] == player_symbol:
        return True
    elif board[0][2] == player_symbol and board[1][2] == player_symbol and board[2][2] == player_symbol:
        return True
    else:
        return False


def diagonal_win_condition(board, player_symbol):
    if board[0][0] == player_symbol and board[1][1] == player_symbol and board[2][2] == player_symbol:
        return True
    elif board[0][2] == player_symbol and board[1][1] == player_symbol and board[2][0] == player_symbol:
        return True
    else:
        return False


def tie(board):
    for row in board:
        for i in row:
            if i == '-':
                return False
    return True


def check_win_condition(board, player_symbol):
    if horizontal_win_condition(board, player_symbol) or vertical_win_condition(board, player_symbol) or diagonal_win_condition(board, player_symbol):
        return True
    else:
        return False


def user_input(coordinate, board, player_symbol):
    board[coordinate[0]].pop(coordinate[1])
    board[coordinate[0]].insert(coordinate[1], player_symbol)
    return board


def start_game():
    game_board = [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]
    return game_board


if __name__ == '__main__':
    start_game()
