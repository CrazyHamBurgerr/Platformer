from scripts.utils import load_image
import unittest
import pygame

# running this test will load a pygame window as it's required for image loading

class TestLoadImageFunction(unittest.TestCase):
    def setUp(self):
        pygame.display.set_caption("utils test")
        pygame.display.set_mode((320, 240))

    def test_invalid_file_path(self):
        self.assertRaises(FileNotFoundError, load_image, 'gabagool')

    def test_ivalid_input_number(self):
        self.assertRaises(TypeError, load_image, 1)
    
    def test_ivalid_input_none(self):
        self.assertRaises(TypeError, load_image, None)
    
    def test_ivalid_input_bool(self):
        self.assertRaises(TypeError, load_image, True)
    
    def test_valid_file(self):
        self.assertTrue(load_image('background.png'))

if __name__ == '__main__':
    unittest.main(verbosity = 2)