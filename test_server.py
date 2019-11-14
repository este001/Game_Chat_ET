import server

"""file for running PyTests"""


def test_username_exists():

    username1 = 'Testname1'
    username2 = 'Testname2'

    test_dict = {}
    test_dict['Client_socket'] = username1

    expected_result1 = True
    expected_result2 = False
    actual_result1 = server.username_exists(username1, test_dict)
    actual_result2 = server.username_exists(username2, test_dict)

    assert expected_result1 == actual_result1
    assert expected_result2 == actual_result2