import unittest
from unittest.mock import patch, MagicMock
import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
from PIL import Image, ImageTk

class TestImageLoader(unittest.TestCase):

    def setUp(self):
        self.label = tk.Label()
        self.T = tk.Text()

    @patch('tkinter.filedialog.askopenfilename', return_value='test_image.jpg')
    @patch('cv2.imread', return_value=(400, 800, 3))
    @patch('PIL.Image.open')
    @patch('PIL.ImageTk.PhotoImage')
    def test_open_image_success(self, mock_photo, mock_image_open, mock_cv2_imread, mock_file_dialog):
        image_loader = ImageLoader()
        image_loader.open_image(self.label, self.T)
        mock_file_dialog.assert_called_once()
        mock_cv2_imread.assert_called_once_with('test_image.jpg')
        mock_image_open.assert_called_once_with('test_image.jpg')
        mock_photo.assert_called_once_with(mock_image_open.return_value.resize.return_value)
        self.label.config.assert_called_once_with(image=mock_photo.return_value)
        self.label.place.assert_called_once_with(relx=0.63, rely=0.12, anchor='center')
        self.assertEqual(self.T.get("1.0", tk.END), 'test_image.jpg')
        messagebox.showinfo.assert_called_once_with(title="InfoMessage", message="Image uploaded successfully")

    @patch('tkinter.filedialog.askopenfilename', return_value=None)
    def test_open_image_cancel(self, mock_file_dialog):
        image_loader = ImageLoader()
        image_loader.open_image(self.label, self.T)
        mock_file_dialog.assert_called_once()
        messagebox.showerror.assert_called_once_with(title="ErrorMessage", message="Error while loading")

    @patch('tkinter.filedialog.askopenfilename', return_value='test_image.jpg')
    @patch('cv2.imread', side_effect=Exception('Error while reading image'))
    def test_open_image_cv2_error(self, mock_cv2_imread, mock_file_dialog):
        image_loader = ImageLoader()
        image_loader.open_image(self.label, self.T)
        mock_file_dialog.assert_called_once()
        mock_cv2_imread.assert_called_once_with('test_image.jpg')
        messagebox.showerror.assert_called_once_with(title="ErrorMessage", message="Error while loading")

    @patch('tkinter.filedialog.askopenfilename', return_value='test_image.jpg')
    @patch('cv2.imread', return_value=(1000, 1000, 3))
    @patch('PIL.Image.open')
    @patch('PIL.ImageTk.PhotoImage')
    def test_open_image_resize(self, mock_photo, mock_image_open, mock_cv2_imread, mock_file_dialog):
        image_loader = ImageLoader()
        image_loader.open_image(self.label, self.T)
        mock_file_dialog.assert_called_once()
        mock_cv2_imread.assert_called_once_with('test_image.jpg')
        mock_image_open.assert_called_once_with('test_image.jpg')
        mock_image_open.return_value.resize.assert_called_once_with((800, 400), Image.ANTIALIAS)
        mock_photo.assert_called_once_with(mock_image_open.return_value.resize.return_value)
        self.label.config.assert_called_once_with(image=mock_photo.return_value)
        self.label.place.assert_called_once_with(relx=0.63, rely=0.12, anchor='center')
        self.assertEqual(self.T.get("1.0", tk.END), 'test_image.jpg')
        messagebox.showinfo.assert_called_once_with(title="InfoMessage", message="Image uploaded successfully")

if __name__ == '__main__':
    unittest.main()