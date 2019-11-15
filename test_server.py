import server
import unittest


class ServerTest(unittest.TestCase):

    def test_users_online_message(self):
        clients = {'client1': 'tim', 'client2': 'este', 'client3': 'oscar'}

        list_of_users = server.online_users(clients)
        expected_list_of_users = "Otim este oscar "

        self.assertEqual(list_of_users, expected_list_of_users)


if __name__ == '__main__':
    unittest.main()
