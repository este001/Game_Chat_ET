import unittest
import tic_tac_toe as ttt


class GameTest(unittest.TestCase):

    def test_start_game(self):
        expected_result = [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]
        actual_result = ttt.start_game()
        self.assertEqual(expected_result, actual_result)

    def test_user_input(self):

        board = ttt.start_game()
        result = ttt.user_input((1, 0), board, player_symbol='x')
        expected_result = [['-', '-', '-'], ['x', '-', '-'], ['-', '-', '-']]

        self.assertEqual(result, expected_result)

    def test_horizontal_win_condition(self):

        symbol = 'x'
        symbol2 = 'o'
        board_top_row = [['x', 'x', 'x'], ['-', '-', '-'], ['-', '-', '-']]
        board_middle_row = [['-', '-', '-'], ['o', 'o', 'o'], ['-', '-', '-']]
        board_bottom_row = [['-', '-', '-'], ['-', '-', '-'], ['x', 'x', 'x']]
        result_top = ttt.horizontal_win_condition(board_top_row, symbol)
        result_middle = ttt.horizontal_win_condition(board_middle_row, symbol2)
        result_bottom = ttt.horizontal_win_condition(board_bottom_row, symbol)

        board_no_win = [['-', '-', '-'], ['-', 'o', '-'], ['x', 'o', 'x']]
        result_no_win = ttt.horizontal_win_condition(board_no_win, symbol)

        expected_result_true = True
        expected_result_false = False

        self.assertEqual(result_top, expected_result_true)
        self.assertEqual(result_middle, expected_result_true)
        self.assertEqual(result_bottom, expected_result_true)

        self.assertEqual(result_no_win, expected_result_false)

    def test_vertical_win_condition(self):

        game_board1 = [['x', '-', '-'], ['x', '-', '-'], ['x', '-', '-']]
        game_board2 = [['-', 'x', '-'], ['-', 'x', '-'], ['-', 'x', '-']]
        game_board3 = [['-', '-', 'x'], ['-', '-', 'x'], ['-', '-', 'x']]
        game_board4 = [['-', '-', 'x'], ['-', '-', 'x'], ['-', '-', 'o']]
        player_symbol = 'x'

        self.assertTrue(ttt.vertical_win_condition(game_board1, player_symbol))
        self.assertTrue(ttt.vertical_win_condition(game_board2, player_symbol))
        self.assertTrue(ttt.vertical_win_condition(game_board3, player_symbol))
        self.assertFalse(ttt.vertical_win_condition(game_board4, player_symbol))

    def test_diagonal_win_condition(self):

        game_board1 = [['x', '-', '-'], ['-', 'x', '-'], ['-', '-', 'x']]
        game_board2 = [['-', '-', 'x'], ['-', 'x', '-'], ['x', '-', '-']]
        game_board3 = [['-', '-', 'o'], ['-', 'x', '-'], ['x', '-', '-']]
        player_symbol = 'x'

        self.assertTrue(ttt.diagonal_win_condition(game_board1, player_symbol))
        self.assertTrue(ttt.diagonal_win_condition(game_board2, player_symbol))
        self.assertFalse(ttt.diagonal_win_condition(game_board3, player_symbol))

    def test_tie(self):
        game_board1 = [['x', 'x', 'o'], ['o', 'o', 'x'], ['x', 'o', 'x']]
        game_board2 = [['x', 'x', 'o'], ['o', 'o', 'x'], ['x', 'o', '-']]

        self.assertTrue(ttt.tie(game_board1))
        self.assertFalse(ttt.tie(game_board2))

    def test_check_win_condition(self):

        vertical_board = [['x', '-', '-'], ['x', '-', '-'], ['x', '-', '-']]
        horizontal_board = [['x', 'x', 'x'], ['-', '-', '-'], ['-', '-', '-']]
        diagonal_board = [['x', '-', '-'], ['-', 'x', '-'], ['-', '-', 'x']]
        no_win_board = [['x', '-', 'o'], ['o', '-', 'x'], ['x', 'o', '-']]
        player_symbol = 'x'

        self.assertTrue(ttt.check_win_condition(vertical_board,player_symbol))
        self.assertTrue(ttt.check_win_condition(horizontal_board, player_symbol))
        self.assertTrue(ttt.check_win_condition(diagonal_board, player_symbol))
        self.assertFalse(ttt.check_win_condition(no_win_board, player_symbol))


if __name__ == '__main__':
    unittest.main()
