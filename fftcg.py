from selenium.common.exceptions import ElementNotVisibleException, ElementNotSelectableException
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
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
    with open(filename + ".html", "w") as file:
        file.write(str(contents))
    return


def getImg(link):
    imgs = link.find_all('div', {'class': 'col image'})
    imglink = imgs[0].find('img').get('src')
    return imglink


def getText(link):
    card_dict = {}

    # find where the card details are stored, under class 'col details'
    elements = link.find_all('div', {'class': 'col details'})

    # elements datatype is ResultSet, must use elements[0] to use the find method
    # find all span tags with class 'items
    # for each item, get text and split them with the ':' and store it in a list
    img_text = [item.getText().split(':') for item in elements[0].find_all('span', {'class': 'item'})]

    # convert list to dictionary
    for i in img_text:
        card_dict.update({i[0]: i[1]})

    # find all 'class with name starting with 'icon'
    eletype = elements[0].findAll("span", {"class": lambda L: L and L.startswith('icon ')})

    # eletype is a dictionary, simply get the 'class' and element [1]
    card_dict['Element'] = eletype[0].get('class')[1]
    return card_dict


def getTitle(link):
    img_title = link.findAll('span', {'class': 'title'})[0].getText()
    return img_title


def getTotalCards(link):
    total_cards = link.findAll('span', {'class': 'num'})[0].getText()
    # split text by "/"
    total_cards = total_cards.split('/')[1]
    return total_cards


url = 'https://fftcg.square-enix-games.com/en/card-browser'
base_url = 'https://fftcg.square-enix-games.com/en/'

# get web driver
driver = getdriver(headless=False)
driver.get(url)
driver.maximize_window()

# wait for the page to load
# find and click the search button
# <button type="submit" class="noselect search-btn"><span class="icon fas fa-search"></span>Search</button>
# //*[@id="browser"]/div[1]/div[3]/button
# <span class="icon fas fa-search"></span>
submit_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//button[@type="submit"]/span[@class="icon fas fa-search"]')))
time.sleep(3)

# submit_button = driver.find_element_by_xpath('//button[@type="submit"]/span[@class="icon fas fa-search"]')
submit_button.click()

time.sleep(5)
# find and click on the first element
firstelement_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="browser"]/div[3]/div[2]')))
# driver.implicitly_wait(10)
firstelement_button.click()

next_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="browser"]/div[4]/div[1]/span[3]')))

first_page = BeautifulSoup(driver.page_source, 'html.parser')
num_cards = int(getTotalCards(first_page))

for i in range(10):
    # cook soup with driver
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    print(getTitle(soup) + " " + getText(soup)['Code'])
    next_button.click()

# end the Selenium browser session
driver.quit()
