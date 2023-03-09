import os
import sys
import time
import csv
import copy
import json
import logging

from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException, \
    ElementClickInterceptedException
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait


def get_driver_path():
    if sys.platform == 'win32':
        driver_path = os.path.join('C:', 'Program Files', 'chromedriver.exe')
    elif sys.platform in ['darwin', 'linux']:
        driver_path = os.path.join('/', 'usr', 'local', 'bin', 'chromedriver')
    else:
        exit()
    return driver_path


def get_chrome_options(headless=True):
    opts = Options()
    if headless:
        opts.add_argument("--headless")  # Operating in headless mode
    else:
        opts.add_argument("--start-maximized")  # max windows
    return opts


def get_driver(headless=True):
    driver_path = get_driver_path()
    opts = get_chrome_options(headless)
    soup_driver = Chrome(options=opts, executable_path=driver_path)
    return soup_driver


def driver_open_tab(soup_driver):
    # open tab
    # You can use (Keys.CONTROL + 't') on other OSs
    soup_driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.COMMAND + 't')
    return


def driver_close_tab(soup_driver):
    # close the tab
    # (Keys.CONTROL + 'w') on other OSs.
    soup_driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.COMMAND + 'w')
    return


def write_html(filename, contents):
    # helper function, dump browser's current html content to file
    with open(filename + ".html", "w") as html_file:
        html_file.write(str(contents))
    return


def get_card_img(link):
    # fftcg page specific - find image function
    images = link.find_all('div', {'class': 'col image'})
    image_link = images[0].find('img').get('src')
    return image_link


def get_card_text(link):
    # fftcg page specific - find text function
    card_dict = {}

    # find where the card details are stored, under class 'col details'
    elements = link.find_all('div', {'class': 'col details'})

    # elements datatype is ResultSet, must use elements[0] to use the find method
    # find all span tags with class 'items
    # for each item, get text and split them with the ':' and store it in a list
    img_text = [item.getText().split(':') for item in elements[0].find_all('tr')]

    # convert list to dictionary
    for item in img_text:
        card_dict.update({item[0]: item[1]})

    # find all 'class with name starting with 'icon'
    element_type = elements[0].findAll("span", {"class": lambda l: l and l.startswith('icon ')})

    # element_type is a dictionary, simply get the 'class' and element [1]
    # element could be empty
    try:
        card_dict['Element'] = element_type[0].get('class')[1]
    except IndexError as ex:
        logging.debug('Exception ' + str(ex))
        card_dict['Element'] = ""
    return card_dict


def get_card_title(link):
    # fftcg page specific - find card title function
    img_title = link.findAll('span', {'class': 'title'})[0].getText()
    return img_title


def get_total_cards(link):
    # fftcg page specific - find title function
    total_cards = link.findAll('span', {'class': 'num'})[0].getText()
    # split text by "/"
    total_cards = total_cards.split('/')[1]
    return total_cards


def click_xpath_fast(soup_driver, xpath):
    # click on an element on a website, without delay
    button = WebDriverWait(soup_driver, 10).until(
        ec.element_to_be_clickable((By.XPATH, xpath)))
    try:
        button.click()
    except StaleElementReferenceException as ex:
        logging.debug('Exception ' + str(ex) + ' while trying click the button' + xpath +
                      ', trying to find element again')
        button = soup_driver.find_element(By.XPATH, xpath)
        button.click()
    return button


def click_xpath(soup_driver, xpath):
    # click on an element on a website, with delay
    logging.info('sleep 5 before searching')
    time.sleep(5)
    button = soup_driver.find_element(By.XPATH, xpath)
    try:
        logging.info('clicking button ' + xpath)
        button.click()

    except NoSuchElementException or StaleElementReferenceException as ex:
        logging.debug('Exception ' + str(ex) + ' while trying click the button' + xpath +
                      ', trying to find element again')
#        button = WebDriverWait(soup_driver, 10).until(
#            ec.element_to_be_clickable((By.XPATH, xpath)))

        ignored_exceptions = (NoSuchElementException, StaleElementReferenceException,)
        button = WebDriverWait(soup_driver, 10, ignored_exceptions=ignored_exceptions) \
            .until(ec.presence_of_element_located((By.XPATH, xpath)))
        button.click()
    except TimeoutException as ex:
        logging.debug('Exception ' + str(ex) + ' while trying click the button' + xpath +
                      ', trying to find element again')
        soup_driver.quit()

    except ElementClickInterceptedException as ex:
        logging.debug('Exception ' + str(ex) + ' while trying click the button' + xpath +
                      ', element not clickable')
        soup_driver.quit()
        exit()

    return button


# setting up level of debugging; will print in console
logging.basicConfig(stream=sys.stderr, level=logging.ERROR)

url = 'https://fftcg.square-enix-games.com/en/card-browser'
base_url = 'https://fftcg.square-enix-games.com/en/'

# get web driver
driver = get_driver(headless=False)

logging.info('getting url')
driver.get(url)
logging.info('max window')
driver.maximize_window()
# wait for the page to load
# find and click the search button

logging.info('setting up search button')
# TODO Implement auto find xpath for search button
submit_button_xpath = '/html/body/section/section/div/div[2]/div/div[1]/div[3]/button'
submit_button = click_xpath(driver, submit_button_xpath)

# find and click on the first element
logging.info('setting up first element button')
# time.sleep(1.0)
first_element_button_xpath = '//*[@id="browser"]/div[3]/div[2]'
first_element_button = click_xpath(driver, first_element_button_xpath)

# find the next button
logging.info('setting up next button')
next_button_xpath = '//*[@id="browser"]/div[4]/div[1]/span[3]'

# this is the first card's page
card_page = BeautifulSoup(driver.page_source, 'html.parser')
num_cards = int(get_total_cards(card_page))
card_list = []
card = {}

for i in range(num_cards):
    # cook soup with driver
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # setup new dictionary for the current card
    card['Title'] = get_card_title(soup)
    card['Image_full'] = get_card_img(soup)
    card['Image_thumb'] = card['Image_full'].replace('full', 'thumb')
    card.update(get_card_text(soup))

    # copy dictionary by value using copy.deepcopy (default is by reference)
    card_list.append(copy.deepcopy(card))

    # print(getCardTitle(soup) + " " + getCardText(soup)['Code'])
    logging.info(card['Title'], card['Code'])

    # dump the card_list dictionary to json file
    with open('card_list.json', 'w') as file:
        file.write(json.dumps(card_list))  # use `json.loads` to do the reverse

    # click for next card
    next_button = click_xpath_fast(driver, next_button_xpath)
    time.sleep(0.5)

# write data to csv file
# use dictionary keys as csv header
csv_columns = list(card)

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
