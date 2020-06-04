from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

headless_mode = True
url = 'http://www.dbzcollection.fr/v2/cartes.php?idc=18'
base_url = 'http://www.dbzcollection.fr/v2/'

if headless_mode:
    opts = Options()
    opts.headless = True
    assert opts.headless  # Operating in headless mode
    driver = Chrome(options=opts, executable_path='/opt/WebDriver/bin/chromedriver')
    driver.get(url)
else:
    driver = Chrome(executable_path='/opt/WebDriver/bin/chromedriver')
    driver.get(url)

report_level1 = []

# Selenium hands the page source to Beautiful Soup (type = BeautifulSoup)
soup_level1 = BeautifulSoup(driver.page_source, 'html.parser')

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
        report_level1.append(result)

# add base_url in front of each string
report_level1 = [base_url + ele for ele in report_level1]

# print report
print(report_level1)

for each_link in report_level1:
    # open tab
    driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 't')
    # You can use (Keys.CONTROL + 't') on other OSs

    # Load a page
    driver.get(each_link)
    sub_soup_level1 = BeautifulSoup(driver.page_source, 'html.parser')


    # close the tab
    # (Keys.CONTROL + 'w') on other OSs.
    driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 'w')

# end the Selenium browser session
driver.quit()
