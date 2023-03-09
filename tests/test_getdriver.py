import unittest
import os
from unittest.mock import patch
from selenium.webdriver.chrome.options import Options
from collection_scraper.fftcg import get_driver, get_driver_path, get_chrome_options


class TestGetDriver(unittest.TestCase):
    @patch('selenium.webdriver.Chrome')
    def test_get_driver(self, mock_chrome):
        # Test that get_driver function returns a Chrome driver instance
        driver = get_driver()
        self.assertIsInstance(driver, type(mock_chrome.return_value))

    def test_get_driver_path(self):
        # Test that get_driver_path function returns a valid path
        driver_path = get_driver_path()
        self.assertTrue(os.path.exists(driver_path))

    def test_get_chrome_options(self):
        # Test that get_chrome_options function returns an Options instance with the correct arguments
        opts = get_chrome_options()
        self.assertIsInstance(opts, Options)
        self.assertIn('--headless', opts.arguments)


if __name__ == '__main__':
    unittest.main()
