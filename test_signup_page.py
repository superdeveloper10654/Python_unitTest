import unittest
import tkinter as tk
from tkinter import ttk
import sqlite3
from PlayerDetection import SignupPage

class TestSignupPage(unittest.TestCase):

    def setUp(self):
        self.root = tk.Tk()
        self.signup_page = SignupPage(self.root, None)

    def test_username_empty(self):
        self.signup_page.signup("", "test@test.com", "password", "password", ttk.Label(self.root))
        self.assertEqual(self.signup_page.lblWarning.cget("text"), "Username field must not be empty.")

    def test_email_empty(self):
        self.signup_page.signup("testuser", "", "password", "password", ttk.Label(self.root))
        self.assertEqual(self.signup_page.lblWarning.cget("text"), "Email field must not be empty.")

    def test_password_empty(self):
        self.signup_page.signup("testuser", "test@test.com", "", "password", ttk.Label(self.root))
        self.assertEqual(self.signup_page.lblWarning.cget("text"), "Password field must not be empty.")

    def test_password_confirmation_empty(self):
        self.signup_page.signup("testuser", "test@test.com", "password", "", ttk.Label(self.root))
        self.assertEqual(self.signup_page.lblWarning.cget("text"), "Password Confirmation field must not be empty.")

    def test_passwords_do_not_match(self):
        self.signup_page.signup("testuser", "test@test.com", "password1", "password2", ttk.Label(self.root))
        self.assertEqual(self.signup_page.lblWarning.cget("text"), "Passwords do not match. Enter matching passwords.")

    def test_successful_registration(self):
        self.signup_page.signup("testuser", "test@test.com", "password", "password", ttk.Label(self.root))
        self.assertEqual(self.signup_page.lblWarning.cget("text"), "Successfully Registered.")

    def tearDown(self):
        self.root.destroy()

if __name__ == '__main__':
    unittest.main()