import server
import unittest


class ServerTest(unittest.TestCase):

    def test_users_online_message(self):
        clients = {'client1': 'tim', 'client2': 'este', 'client3': 'oscar'}

        list_of_users = server.online_users(clients)
        expected_list_of_users = "Otim-este-oscar-"

        self.assertEqual(list_of_users, expected_list_of_users)

    def test_strip_header(self):
        message = "STim has connected"
        expected_result = "Tim has connected"
        actual_result = server.strip_header(message)

        self.assertEqual(actual_result, expected_result)


if __name__ == '__main__':
    unittest.main()
