import unittest
import cv2
from unittest.mock import patch, MagicMock
from tkinter import messagebox

class MyApp:
    def __init__(self):
        self.resultImg = None
        self.image_path_save = None

    def save_app(self):
        global resultImg
        try:
            resultImg = cv2.cvtColor(resultImg, cv2.COLOR_BGR2RGB) # convert image to RGB because algorithm returns it in BGR format
            cv2.imwrite(image_path_save+"/savedImg.jpg", resultImg) # save image in selected path
            messagebox.showinfo(title="InfoMessage", message="Image saved successfully") # create messagebox with saved successful as message for user
        except:
            messagebox.showerror(title="ErrorMessage", message="Error while saving")# create messagebox with error while saving for user


class TestSaveApp(unittest.TestCase):

    @patch('cv2.cvtColor')
    @patch('cv2.imwrite')
    @patch.object(messagebox, 'showinfo')
    def test_save_success(self, mock_showinfo, mock_imwrite, mock_cvtColor):
        # Arrange
        app = MyApp()
        app.resultImg = MagicMock()
        app.image_path_save = "/path/to/save"
        mock_cvtColor.return_value = MagicMock()
        mock_imwrite.return_value = True

        # Act
        app.save_app()

        # Assert
        mock_cvtColor.assert_called_once_with(app.resultImg, cv2.COLOR_BGR2RGB)
        mock_imwrite.assert_called_once_with("/path/to/save/savedImg.jpg", mock_cvtColor.return_value)
        mock_showinfo.assert_called_once_with(title="InfoMessage", message="Image saved successfully")

    @patch('cv2.cvtColor')
    @patch('cv2.imwrite')
    @patch.object(messagebox, 'showerror')
    def test_save_app_error(self, mock_showerror, mock_imwrite, mock_cvtColor):
        # Arrange
        app = MyApp()
        app.resultImg = MagicMock()
        app.image_path_save = "/path/to/save"
        mock_cvtColor.return_value = MagicMock()
        mock_imwrite.side_effect = Exception("Error while saving")

        # Act
        app.save_app()

        # Assert
        mock_cvtColor.assert_called_once_with(app.resultImg, cv2.COLOR_BGR2RGB)
        mock_imwrite.assert_called_once_with("/path/to/save/savedImg.jpg", mock_cvtColor.return_value)
        mock_showerror.assert_called_once_with(title="ErrorMessage", message="Error while saving")

if __name__ == '__main__':
    unittest.main()