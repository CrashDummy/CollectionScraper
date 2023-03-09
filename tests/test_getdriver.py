import unittest
from selenium.webdriver import Chrome
from collection_scraper.fftcg import getdriver


class TestGetDriver(unittest.TestCase):
    def test_headless(self):
        driver = getdriver(headless=True)
        self.assertIsInstance(driver, Chrome)
        driver.quit()

    def test_not_headless(self):
        driver = getdriver(headless=False)
        self.assertIsInstance(driver, Chrome)
        driver.quit()


if __name__ == '__main__':
    unittest.main()
