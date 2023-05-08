import unittest
from unittest.mock import MagicMock
from PIL import Image
import numpy as np

class TestProcess(unittest.TestCase):
    def setUp(self):
        self.label = MagicMock()
        self.image_path = "test.jpg"
        self.resultImg = None

    def test_process_success(self):
        # Mock the apply function to return a test image
        apply_mock = MagicMock(return_value=np.zeros((100, 100, 3), dtype=np.uint8))
        with unittest.mock.patch("__main__.apply", apply_mock):
            # Call the process function
            process(self.label, self.image_path)
            # Check that the label image was set correctly
            self.label.config.assert_called_once()
            args, kwargs = self.label.config.call_args
            self.assertIsInstance(kwargs["image"], ImageTk.PhotoImage)
            # Check that the global result image was set correctly
            self.assertIsNotNone(resultImg)
            self.assertEqual(resultImg.shape, (100, 100, 3))
            # Check that the success message was shown
            messagebox.showinfo.assert_called_once_with(title="InfoMessage", message="Player detection successful")

    def test_process_failure(self):
        # Mock the apply function to raise an exception
        apply_mock = MagicMock(side_effect=Exception("Test error"))
        with unittest.mock.patch("__main__.apply", apply_mock):
            # Call the process function
            process(self.label, self.image_path)
            # Check that the error message was shown
            messagebox.showerror.assert_called_once_with(title="ErrorMessage", message="Error while detecting")