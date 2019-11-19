import unittest
import tic_tac_toe as ttt


class GameTest(unittest.TestCase):
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


if __name__ == '__main__':
    unittest.main()
