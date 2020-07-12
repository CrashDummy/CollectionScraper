import logging
import sys
import time
import csv
import copy

from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def getdriver(headless=True):
    driverpath = '/opt/WebDriver/bin/chromedriver'

    if headless:
        opts = Options()
        opts.headless = True
        assert opts.headless  # Operating in headless mode
        driver = Chrome(options=opts, executable_path=driverpath)
    else:
        driver = Chrome(executable_path=driverpath)
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
    except StaleElementReferenceException as ex:
        logging.debug('Exception ' + str(ex) + ' while trying click the button' + xpath +
                      ', trying to find element again')
        button = driver.find_element_by_xpath(xpath)
        button.click()
    return button


def clickXPath(driver, xpath):
    logging.info('sleep 5 before searching')
    time.sleep(5)
    button = driver.find_element_by_xpath(xpath)
    try:
        logging.info('clicking button ' + xpath)
        button.click()

    except NoSuchElementException or StaleElementReferenceException as ex:
        logging.debug('Exception ' + str(ex) + ' while trying click the button' + xpath +
                      ', trying to find element again')
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xpath)))

        ignored_exceptions = (NoSuchElementException, StaleElementReferenceException,)
        button = WebDriverWait(driver, 10, ignored_exceptions=ignored_exceptions) \
            .until(EC.presence_of_element_located((By.XPATH, xpath)))
        button.click()
    except TimeoutException as ex:
        logging.debug('Exception ' + str(ex) + ' while trying click the button' + xpath +
                      ', trying to find element again')
        driver.quit()
        exit()

    return button


logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

url = 'https://fftcg.square-enix-games.com/en/card-browser'
base_url = 'https://fftcg.square-enix-games.com/en/'

# get web driver
driver = getdriver(headless=True)

logging.info('getting url')
driver.get(url)
logging.info('max window')
driver.maximize_window()
# wait for the page to load
# find and click the search button

logging.info('setting up search button')
submit_button_xpath = '//button[@type="submit"]/span[@class="icon fas fa-search"]'
submit_button = clickXPath(driver, submit_button_xpath)

# find and click on the first element
logging.info('setting up first element button')
firstelement_button_xpath = '//*[@id="browser"]/div[3]/div[2]'
firstelement_button = clickXPath(driver, firstelement_button_xpath)

# find the next button
logging.info('setting up next button')
next_button_xpath = '//*[@id="browser"]/div[4]/div[1]/span[3]'

# this is the first card's page
card_page = BeautifulSoup(driver.page_source, 'html.parser')
num_cards = int(getTotalCards(card_page))
card_list = []


for i in range(num_cards):
    # cook soup with driver
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # setup new dictionary for the current card
    card = {}
    card['Title'] = getCardTitle(soup)
    card['Image_full'] = getCardImg(soup)
    card['Image_thumb'] = card['Image_full'].replace('full', 'thumb')
    card.update(getCardText(soup))

    # copy dictionary by value (default is by reference)
    card_list.append(copy.deepcopy(card))

    # print(getCardTitle(soup) + " " + getCardText(soup)['Code'])
    logging.info(card['Title'], card['Code'])

    # click for next card
    next_button = clickXPath_fast(driver, next_button_xpath)
    time.sleep(0.5)

# write data to csv file
csv_columns = ['Title', 'Image_full', 'Image_thumb', 'Type', 'Job', 'Element', 'Cost', 'Rarity', 'Power', 'Category',
               'Set', 'Code']
csv_file = "ff_card_list.csv"
try:
    with open(csv_file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for each_card in card_list:
            writer.writerow(each_card)
except IOError:
    logging.error("I/O error")


# end the Selenium browser session
driver.quit()