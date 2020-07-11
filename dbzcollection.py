from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
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


url = 'http://www.dbzcollection.fr/v2/cartes.php?idc=18'
base_url = 'http://www.dbzcollection.fr/v2/'

# get web driver
webdriver = getdriver(headless=False)
webdriver.get(url)

# cook soup with driver
# search for all <div class="bloc_capsule"> then search for all <a href> links
report_level1 = cooksoup_level1(webdriver, firstSearchTag='div', firstSearchClass='bloc_capsule', thenSerach='a', thenGet='href')

for each_link in report_level1:
    # Load a page
    webdriver.get(each_link)
    report_level2 = cooksoup_level1(webdriver, firstSearchTag='td', firstSearchClass='cadre_carte1', thenSerach='img', thenGet='src')

# table = soup.find(lambda tag: tag.name=='table' and tag.find(lambda ttag: ttag.name=='th' and ttag.text=='Common Name'))

# table = soup_levelxx.find_all('table', class_='table_carte', attrs='img')

# end the Selenium browser session
webdriver.quit()