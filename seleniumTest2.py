from selenium.common.exceptions import ElementNotVisibleException, ElementNotSelectableException
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import os


def getdriver(headless=True):
    if headless:
        opts = Options()
        opts.headless = True
        assert opts.headless  # Operating in headless mode
        driver = Chrome(options=opts, executable_path='/opt/WebDriver/bin/chromedriver')
    else:
        driver = Chrome(executable_path='/opt/WebDriver/bin/chromedriver')
    return driver


def cooksoup_level1(driver, firstSearchTag, firstSearchClass, thenSerach, thenGet):
    report = []

    # Selenium hands the page source to Beautiful Soup (type = BeautifulSoup)
    soup_level1 = BeautifulSoup(driver.page_source, 'html.parser')

    # find all matching key items (type = ResultSet, iterable)
    soup_level2 = soup_level1.find_all(firstSearchTag, {'class': firstSearchClass})
    # results = soup_level1.find_all(class_='bloc_capsule')

    # iterate through ResultSet and find tag "a"
    for soup_level3 in soup_level2:
        soup_level4 = soup_level3.find(thenSerach)

        # shall there are results of the find, store it in the report
        if soup_level4 is not None:
            result = soup_level4.get(thenGet)
            # append report list
            report.append(result)

    # add base_url in front of each string
    report = [base_url + ele for ele in report]

    # print report
    print(report)

    return report


def driverOpenTab(soupdriver):
    # open tab
    soupdriver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 't')
    # You can use (Keys.CONTROL + 't') on other OSs
    return


def driverCloseTab(soupdriver):
    # close the tab
    # (Keys.CONTROL + 'w') on other OSs.
    soupdriver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 'w')
    return


def writeToHTML(filename, contents):
    with open(filename+".html", "w") as file:
        file.write(str(contents))
    return


def getImg(link):
    imgs = link.find_all('div', {'class': 'col image'})
    imglink = imgs[0].find('img').get('src')
    return imglink


def getText(link):
    elements = link.find_all('div', {'class': 'col details'})
    imgText = [items.getText() for items in elements[0].find_all('span')]
    return imgText


def getTitle(link):
    imgTitle = link.findAll('span', {'class': 'title'})[0].getText()
    return imgTitle


url = 'https://fftcg.square-enix-games.com/en/card-browser'
base_url = 'https://fftcg.square-enix-games.com/en/'

# get web driver
driver = getdriver(headless=False)
driver.get(url)

# wait for the page to load
# find and click the search button
submit_button = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="browser"]/div[1]/div[3]/button')))
submit_button.click()

# find and click on the first element
firstelement_button = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="browser"]/div[3]/div[2]')))
firstelement_button.click()

# cook soup with driver
soup_level1 = BeautifulSoup(driver.page_source, 'html.parser')
img = soup_level1.find_all('div', {'class': 'col image'})
imglink = getImgURL(img)

print(imglink)

# end the Selenium browser session
driver.quit()