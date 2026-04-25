from scripts.clouds import Cloud, Clouds
from scripts.utils import load_images
import unittest
import pygame

# running this test will load a pygame window as it's required for image loading

class TestCloudScript(unittest.TestCase):
    def setUp(self):
        pygame.display.set_caption("cloud test")
        pygame.display.set_mode((320, 240))
        self.assets = {
            'clouds': load_images('clouds')
        }
        self.clouds = Clouds(self.assets['clouds'], 3)
        self.cloud = self.clouds.clouds[1]

    def test_cloud_speed(self):
        self.cloud.speed = 1
        self.cloud.pos[0] = 0
        self.cloud.update()
        self.assertEqual(self.cloud.pos[0], self.cloud.speed)

    def test_cloud_attributes(self):
        self.assertLess(self.cloud.pos[0], 100000)
        self.assertLess(self.cloud.pos[1], 100000)
        self.assertLessEqual(0.05, self.cloud.speed)
        self.assertLessEqual(self.cloud.speed, 0.1)
        self.assertLessEqual(0.2, self.cloud.depth)
        self.assertLessEqual(self.cloud.depth, 0.8)
    
    def test_cloud_image(self):
        self.assertIn(self.cloud.img, self.assets['clouds'])

if __name__ == '__main__':
    unittest.main(verbosity = 2)