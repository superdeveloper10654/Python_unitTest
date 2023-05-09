import unittest
import sqlite3
from PlayerDetection import UtilityClass

class TestUtilityClass(unittest.TestCase):

    def setUp(self):
        self.utility = UtilityClass()
        self.con = sqlite3.connect(":memory:")
        self.cursor = self.con.cursor()
        self.cursor.execute("CREATE TABLE USERS (USERNAME TEXT, PASSWORD TEXT)")
        self.cursor.execute("INSERT INTO USERS VALUES ('testuser', 'testpassword')")

    def test_validateLogin_with_valid_credentials(self):
        result, message = self.utility.validateLogin("testuser", "testpassword", self.con)
        self.assertTrue(result)
        self.assertEqual(message, "Successfully Logged in!")

    def test_validateLogin_with_invalid_username(self):
        result, message = self.utility.validateLogin("", "testpassword", self.con)
        self.assertFalse(result)
        self.assertEqual(message, "Username field must not be empty.")

    def test_validateLogin_with_invalid_password(self):
        result, message = self.utility.validateLogin("testuser", "", self.con)
        self.assertFalse(result)
        self.assertEqual(message, "Password field must not be empty.")

    def test_validateLogin_with_unregistered_user(self):
        result, message = self.utility.validateLogin("unknownuser", "unknownpassword", self.con)
        self.assertFalse(result)
        self.assertEqual(message, "You are not registered. Please sign up with new details.")

    def tearDown(self):
        self.con.close()

if __name__ == '__main__':
    unittest.main()