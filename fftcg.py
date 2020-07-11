from selenium.common.exceptions import ElementNotVisibleException, ElementNotSelectableException
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException
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


def getCardImg(link):
    imgs = link.find_all('div', {'class': 'col image'})
    imglink = imgs[0].find('img').get('src')
    return imglink


def getCardText(link):
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


def getCardTitle(link):
    img_title = link.findAll('span', {'class': 'title'})[0].getText()
    return img_title


def getTotalCards(link):
    total_cards = link.findAll('span', {'class': 'num'})[0].getText()
    # split text by "/"
    total_cards = total_cards.split('/')[1]
    return total_cards


def clickXPath_fast(driver, xpath):
    button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, xpath)))
    try:
        button.click()
    except StaleElementReferenceException as Exception:
        print('StaleElementReferenceException while trying click the button' + xpath + ', trying to find element again')
        button = driver.find_element_by_xpath(xpath)
        button.click()
    return button


def clickXPath(driver, xpath):
    print('sleep 5 before searching')
    time.sleep(5)
    button = driver.find_element_by_xpath(xpath)
    try:
        print('clicking button ' + xpath)
        button.click()

    except NoSuchElementException or StaleElementReferenceException as ex:
        print('Exception ' + str(ex) + ' while trying click the button' + xpath + ', trying to find element again')
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xpath)))

        ignored_exceptions = (NoSuchElementException, StaleElementReferenceException,)
        button = WebDriverWait(driver, 10, ignored_exceptions=ignored_exceptions) \
            .until(EC.presence_of_element_located((By.XPATH, xpath)))
        button.click()
    except TimeoutException as ex:
        print('Exception ' + str(ex) + ' while trying click the button' + xpath + ', trying to find element again')
        driver.quit()
        exit()

    return button


url = 'https://fftcg.square-enix-games.com/en/card-browser'
base_url = 'https://fftcg.square-enix-games.com/en/'

# get web driver
driver = getdriver(headless=True)

print('getting url')
driver.get(url)
print('max window')
driver.maximize_window()
# wait for the page to load
# find and click the search button
# <button type="submit" class="noselect search-btn"><span class="icon fas fa-search"></span>Search</button>
# //*[@id="browser"]/div[1]/div[3]/button
# <span class="icon fas fa-search"></span>
# submit_button = WebDriverWait(driver, 10).until(
#    EC.element_to_be_clickable((By.XPATH, '//button[@type="submit"]/span[@class="icon fas fa-search"]')))
# submit_button = driver.find_element_by_xpath('//button[@type="submit"]/span[@class="icon fas fa-search"]')
# submit_button.click()

print('seting up search button')
submit_button_xpath = '//button[@type="submit"]/span[@class="icon fas fa-search"]'
submit_button = clickXPath(driver, submit_button_xpath)

# find and click on the first element
# firstelement_button = WebDriverWait(driver, 10).until(
#    EC.element_to_be_clickable((By.XPATH, '//*[@id="browser"]/div[3]/div[2]')))
# driver.implicitly_wait(10)
# firstelement_button.click()

print('seting up first element button')
firstelement_button_xpath = '//*[@id="browser"]/div[3]/div[2]'
firstelement_button = clickXPath(driver, firstelement_button_xpath)

# find the next button
# next_button = WebDriverWait(driver, 10).until(
#    EC.element_to_be_clickable((By.XPATH, '//*[@id="browser"]/div[4]/div[1]/span[3]')))

print('seting up next button')
next_button_xpath = '//*[@id="browser"]/div[4]/div[1]/span[3]'

# this is the first card's page
card_page = BeautifulSoup(driver.page_source, 'html.parser')
num_cards = int(getTotalCards(card_page))
card_list = {}

for i in range(num_cards):
    # cook soup with driver
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    card_list['Title'] = getCardTitle(soup)
    card_list['Image']= getCardImg(soup)
    card_list.update(getCardText(soup))

    # print(getCardTitle(soup) + " " + getCardText(soup)['Code'])
    print(card_list['Title'], card_list['Code'])
    # click for next card
    next_button = clickXPath_fast(driver, next_button_xpath)

# end the Selenium browser session
driver.quit()
