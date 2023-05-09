import unittest
import sqlite3
from unittest.mock import MagicMock
from PlayerDetection import UtilityClass

class TestUtilityClass(unittest.TestCase):

    def setUp(self):
        self.utility = UtilityClass()
        self.con = sqlite3.connect(':memory:')
        self.cursor = self.con.cursor()
        self.cursor.execute('''CREATE TABLE USERS
                            (ID INT PRIMARY KEY NOT NULL,
                            USERNAME TEXT NOT NULL,
                            PASSWORD TEXT NOT NULL);''')
        self.cursor.execute("INSERT INTO USERS (ID, USERNAME, PASSWORD) VALUES (1, 'testuser', 'testpassword')")
    

    def test_validateLogin_with_valid_credentials(self):
        result, message = self.utility.validateLogin('testuser', 'testpassword', self.con)
        self.assertTrue(result)
        self.assertEqual(message, 'Successfully Logged in!')

    def test_validateLogin_with_invalid_username(self):
        result, message = self.utility.validateLogin('', 'testpassword', self.con)
        self.assertFalse(result)
        self.assertEqual(message, 'Username field must not be empty.')

    def test_validateLogin_with_invalid_password(self):
        result, message = self.utility.validateLogin('testuser', '', self.con)
        self.assertFalse(result)
        self.assertEqual(message, 'Password field must not be empty.')

    def test_validateLogin_with_unregistered_user(self):
        result, message = self.utility.validateLogin('unknownuser', 'unknownpassword', self.con)
        self.assertFalse(result)
        self.assertEqual(message, 'You are not registered. Please sign up with new details.')

    def test_validateLogin_with_sqlite_error(self):
        mock_cursor = MagicMock()
        mock_cursor.execute.side_effect = Exception('SQLite Connection Error occurred!')
        mock_con = MagicMock()
        mock_con.cursor.return_value = mock_cursor
        result, message = self.utility.validateLogin('testuser', 'testpassword', mock_con)
        self.assertFalse(result)
        self.assertEqual(message, 'SQLite Connection Error occurred!')

    def tearDown(self):
        self.con.close()



if __name__ == '__main__':
    unittest.main()