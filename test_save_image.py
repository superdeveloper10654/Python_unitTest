import unittest
import cv2
from unittest.mock import patch, MagicMock
from tkinter import messagebox

class TestSaveApp(unittest.TestCase):

    def setUp(self):
        self.app = App()

    @patch('cv2.cvtColor')
    @patch('cv2.imwrite')
    @patch('tkinter.messagebox.showinfo')
    def test_save_app_success(self, mock_showinfo, mock_imwrite, mock_cvtColor):
        # Arrange
        mock_cvtColor.return_value = MagicMock()
        mock_imwrite.return_value = True

        # Act
        self.app.save_app()

        # Assert
        mock_cvtColor.assert_called_once()
        mock_imwrite.assert_called_once()
        mock_showinfo.assert_called_once_with(title="InfoMessage", message="Image saved successfully")

    @patch('cv2.cvtColor')
    @patch('cv2.imwrite')
    @patch('tkinter.messagebox.showerror')
    def test_save_app_failure(self, mock_showerror, mock_imwrite, mock_cvtColor):
        # Arrange
        mock_cvtColor.return_value = MagicMock()
        mock_imwrite.return_value = False

        # Act
        self.app.save_app()

        # Assert
        mock_cvtColor.assert_called_once()
        mock_imwrite.assert_called_once()
        mock_showerror.assert_called_once_with(title="ErrorMessage", message="Error while saving")

if __name__ == '__main__':
    unittest.main()