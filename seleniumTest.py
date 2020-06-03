from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options

opts = Options()
opts.headless = True
assert opts.headless  # Operating in headless mode
browser = Chrome(options=opts, executable_path='/opt/WebDriver/bin/chromedriver')
browser.get('https://duckduckgo.com')
