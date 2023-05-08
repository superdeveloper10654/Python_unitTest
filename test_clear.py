import unittest

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
        self.assertIsNone(image_path)
        self.assertIsNone(image_path_save)
        self.assertIsNone(resultImg)

if __name__ == '__main__':
    unittest.main()