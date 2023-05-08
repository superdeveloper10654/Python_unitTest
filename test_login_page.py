import unittest
import tkinter as tk
from tkinter import ttk
from tkinter import Tk
from unittest.mock import patch
from PlayerDetection import LoginPage

# class TestLoginPage(unittest.TestCase):

#     def test_username_password_entry_widgets(self):
#         login_page = LoginPage(None, None)
#         assert isinstance(login_page.username_entry, ttk.Entry)
#         assert isinstance(login_page.password_entry, ttk.Entry)

#     def test_login_button(self):
#         login_page = LoginPage(None, None)
#         assert isinstance(login_page.submitbtn, ttk.Button)

#     def test_signup_button(self):
#         login_page = LoginPage(None, None)
#         assert isinstance(login_page.signUpbtn, ttk.Button)

#     def test_check_login_valid_credentials(self):
#         login_page = LoginPage(None, None)
#         result = login_page.checkLogin("testuser", "testpassword", ttk.Label(None))
#         assert result == "Successfully Logged in!"

#     def test_check_login_invalid_credentials(self):
#         login_page = LoginPage(None, None)
#         result = login_page.checkLogin("invaliduser", "invalidpassword", ttk.Label(None))
#         assert result == "You are not registered. Please sign up with new details."


# if __name__ == '__main__':
#     unittest.main()


class TestLoginPage(unittest.TestCase):

    def setUp(self):
        self.root = Tk()
        self.login_page = LoginPage(MockController(), self.root)

    def test_checkLogin_with_empty_username(self):
        self.lblWarning = ttk.Label(self, text ="", background="#fff8eb")
        self.login_page.checkLogin("", "password", lblWarning)
        self.assertEqual(lblWarning.cget("text"), "Username field must not be empty.")

    def test_checkLogin_with_empty_password(self):
        self.lblWarning = ttk.Label(self, text ="", background="#fff8eb")
        self.login_page.checkLogin("username", "", lblWarning)
        self.assertEqual(lblWarning.cget("text"), "Password field must not be empty.")

    @patch('sqlite3.connect')
    def test_checkLogin_with_no_tables(self, mock_connect):
        mock_cursor = mock_connect.return_value.cursor.return_value
        mock_cursor.execute.return_value = []
        self.lblWarning = ttk.Label(self, text ="", background="#fff8eb")
        self.login_page.checkLogin("username", "password", lblWarning)
        self.assertEqual(lblWarning.cget("text"), "You are not registered. Please sign up with new details.")
        mock_connect.assert_called_once_with("users.db")
        mock_cursor.execute.assert_called_once_with("SELECT * FROM sqlite_master;")
        mock_cursor.execute.assert_called_once_with("CREATE TABLE USERS(USERNAME VARCHAR(50),EMAIL VARCHAR(50), PASSWORD VARCHAR(50));")
        mock_connect.return_value.commit.assert_called_once()
        mock_connect.return_value.close.assert_called_once()

    @patch('sqlite3.connect')
    def test_checkLogin_with_valid_credentials(self, mock_connect):
        mock_cursor = mock_connect.return_value.cursor.return_value
        mock_cursor.fetchall.return_value = [("username", "email", "password")]
        # lblWarning = self.login_page.lblWarning
        self.lblWarning = ttk.Label(self, text ="", background="#fff8eb")
        self.login_page.controller = MockController()
        self.login_page.checkLogin("username", "password", lblWarning)
        self.assertEqual(lblWarning.cget("text"), "Successfully Logged in!")
        self.assertIsInstance(self.login_page.controller.frames["ImagePage"], ImagePage)
        mock_connect.assert_called_once_with("users.db")
        mock_cursor.execute.assert_called_once_with("select * from USERS WHERE USERNAME='username' AND PASSWORD = 'password';")
        mock_connect.return_value.commit.assert_called_once()
        mock_connect.return_value.close.assert_called_once()

    @patch('sqlite3.connect')
    def test_checkLogin_with_invalid_credentials(self, mock_connect):
        mock_cursor = mock_connect.return_value.cursor.return_value
        mock_cursor.fetchall.return_value = []
        # lblWarning = self.login_page.lblWarning
        self.lblWarning = ttk.Label(self, text ="", background="#fff8eb")
        self.login_page.checkLogin("username", "password", lblWarning)
        self.assertEqual(lblWarning.cget("text"), "You are not registered. Please sign up with new details.")
        mock_connect.assert_called_once_with("users.db")
        mock_cursor.execute.assert_called_once_with("select * from USERS WHERE USERNAME='username' AND PASSWORD = 'password';")
        mock_connect.return_value.commit.assert_called_once()
        mock_connect.return_value.close.assert_called_once()

class MockController:
    def __init__(self):
        self.frames = {}

    def show_frame(self, frame):
        self.frames[frame.__name__] = frame()

class ImagePage:
    pass

if __name__ == '__main__':
    unittest.main()