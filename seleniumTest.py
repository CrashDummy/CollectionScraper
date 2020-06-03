from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

headless_mode = True
url = 'http://www.dbzcollection.fr/v2/cartes.php?idc=18'

if headless_mode:
    opts = Options()
    opts.headless = True
    assert opts.headless  # Operating in headless mode
    browser = Chrome(options=opts, executable_path='/opt/WebDriver/bin/chromedriver')
    browser.get(url)
else:
    browser = Chrome(executable_path='/opt/WebDriver/bin/chromedriver')
    browser.get(url)

report = []

# Selenium hands the page source to Beautiful Soup (type = BeautifulSoup)
soup_level1 = BeautifulSoup(browser.page_source, 'html.parser')

# find all matching key items (type = ResultSet, iterable)
soup_level2 = soup_level1.find_all('div', {'class': 'bloc_capsule'})
# results = soup_level1.find_all(class_='bloc_capsule')

# iterate through ResultSet and find tag "a"
for soup_level3 in soup_level2:
    soup_level4 = soup_level3.find('a')

    # shall there are results of the find, store it in the report
    if soup_level4 is not None:
        result = soup_level4.get('href')
        # append report list
        report.append(result)

# print report
print(report)

# end the Selenium browser session
browser.quit()
