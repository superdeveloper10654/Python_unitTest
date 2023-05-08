import unittest
from PlayerDetection import LoginPage

class TestLoginPage(unittest.TestCase):

    def test_username_password_entry_widgets(self):
        login_page = LoginPage(None, None)
        assert isinstance(login_page.username_entry, ttk.Entry)
        assert isinstance(login_page.password_entry, ttk.Entry)

    def test_login_button(self):
        login_page = LoginPage(None, None)
        assert isinstance(login_page.submitbtn, ttk.Button)

    def test_signup_button(self):
        login_page = LoginPage(None, None)
        assert isinstance(login_page.signUpbtn, ttk.Button)

    def test_check_login_valid_credentials(self):
        login_page = LoginPage(None, None)
        result = login_page.checkLogin("testuser", "testpassword", ttk.Label(None))
        assert result == "Successfully Logged in!"

    def test_check_login_invalid_credentials(self):
        login_page = LoginPage(None, None)
        result = login_page.checkLogin("invaliduser", "invalidpassword", ttk.Label(None))
        assert result == "You are not registered. Please sign up with new details."


if __name__ == '__main__':
    unittest.main()