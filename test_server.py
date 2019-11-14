import server

"""file for running PyTests"""


def test_username_exists():

    username1 = 'Testname1'
    username2 = 'Testname2'

    test_dict = {}
    test_dict['Client_socket'] = username1

    expected_result_true = True
    expected_result_false = False
    actual_result1 = server.username_exists(username1, test_dict)
    actual_result2 = server.username_exists(username2, test_dict)

    assert expected_result_true == actual_result1
    assert expected_result_false == actual_result2