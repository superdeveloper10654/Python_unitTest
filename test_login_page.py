import unittest
from PlayerDetection import LoginPage

class TestLoginPage(unittest.TestCase):

    def setUp(self):
        self.login_page = LoginPage(None, None)

    def test_empty_fields(self):
        # Test if the warning label shows up when the username and password fields are empty
        self.login_page.checkLogin("", "", self.login_page.lblWarning)
        print(self.login_page.lblWarning['text'])
        self.assertEqual(self.login_page.lblWarning['text'], "Username field must not be empty.")

    def test_valid_login(self):
        # Test if the login button works correctly when valid username and password values are entered
        self.login_page.checkLogin("testuser", "testpassword", self.login_page.lblWarning)
        self.assertEqual(self.login_page.lblWarning['text'], "Successfully Logged in!")