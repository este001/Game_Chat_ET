import client
import unittest

"""Test file for client"""


class ClientTest(unittest.TestCase):

    def test_strip_header(self):
        message = "SHello"
        expected_result = "Hello"
        actual_result = client.strip_header(message)

        self.assertEqual(actual_result, expected_result)

    def test_place_player_mark(self):
        player = 'Tim'
        game_board = [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]
        coordinates = '00'
        player_dict = {'Tim': 'x'}
        expected_result = [['x', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]

        actual_result = client.place_player_mark(player, game_board, coordinates,player_dict)
        self.assertEqual(expected_result, actual_result)

    def test_start_game(self):
        expected_result = [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]
        actual_result = client.start_game()
        self.assertEqual(expected_result, actual_result)

if __name__ == '__main__':
    unittest.main()
