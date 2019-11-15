import client
import unittest

"""Pytest file for client"""


class ClientTest(unittest.TestCase):

    def test_strip_header(self):
        message = "SHello"
        expected_result = "Hello"
        actual_result = client.strip_header(message)

        self.assertEqual(actual_result, expected_result)


unittest.main()
