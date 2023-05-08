import unittest
from unittest.mock import patch
import tkinter as tk
from tkinter import filedialog

class TestOpenImage(unittest.TestCase):

    @patch.object(filedialog, 'askdirectory', return_value='/path/to/directory')
    def test_open_image1(self, mock_askdirectory):
        # create a dummy GUI with a text widget
        root = tk.Tk()
        T1 = tk.Text(root)
        T1.pack()

        # call the function
        open_image1(T1)

        # assert that the global variable is set correctly
        self.assertEqual(image_path_save, '/path/to/directory')

        # assert that the text widget is updated correctly
        expected_text = '/path/to/directory'
        actual_text = T1.get("1.0", tk.END).strip()
        self.assertEqual(actual_text, expected_text)

        # clean up
        root.destroy()

    @patch.object(filedialog, 'askdirectory', return_value='/another/path')
    def test_open_image1_multiple_calls(self, mock_askdirectory):
        # create a dummy GUI with a text widget
        root = tk.Tk()
        T1 = tk.Text(root)
        T1.pack()

        # call the function twice
        open_image1(T1)
        open_image1(T1)

        # assert that the global variable is set correctly
        self.assertEqual(image_path_save, '/another/path')

        # assert that the text widget is updated correctly
        expected_text = '/another/path'
        actual_text = T1.get("1.0", tk.END).strip()
        self.assertEqual(actual_text, expected_text)

        # clean up
        root.destroy()