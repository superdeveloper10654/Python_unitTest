import unittest
from tkinter import Label

def clear_image(label):
    global image_path,resultImg
    label.image=None # set the image to none 
    image_path=None # set the load path to none 
    image_path_save=None # set the save path to none 
    resultImg=None # set the result image variable to none

class TestClearImage(unittest.TestCase):
    def setUp(self):
        self.label = Label()
        self.label.image = "test_image.png"
        self.image_path = "test_image.png"
        self.image_path_save = "test_image_save.png"
        self.resultImg = "test_result.png"

    def test_clear_image(self):
        clear_image(self.label)
        self.assertIsNone(self.label.image)
        self.assertIsNone(self.image_path)
        self.assertIsNone(self.image_path_save)
        self.assertIsNone(self.resultImg)

if __name__ == '__main__':
    unittest.main()