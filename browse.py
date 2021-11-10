from selenium import webdriver
from selenium.webdriver import FirefoxOptions
import os
from bs4 import BeautifulSoup
import requests
import shutil
from datetime import date, timedelta
import time
import pickle

def login(url, samvad_id, samvad_pw, download_dir):
    profile = webdriver.FirefoxProfile()
    profile.set_preference('browser.download.folderList', 2) # custom location
    profile.set_preference("pdfjs.disabled", True)
    profile.set_preference('browser.download.manager.showWhenStarting', False)
    profile.set_preference('browser.download.dir', download_dir)
    profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, application/pdf')

    opts = FirefoxOptions()
    #opts.add_argument("--headless")

    browser = webdriver.Firefox(options=opts, firefox_profile=profile,\
        log_path= download_dir +'geckodriver-v0.29.1-linux64/geckodriver.log', \
        executable_path= download_dir +'geckodriver-v0.29.1-linux64/geckodriver')

    print("Browse: Opening the site samvad.media and attempting to login.")
    browser.get(url)

    username = browser.find_element_by_id('txtUserName')
    password = browser.find_element_by_id('txtPassword')

    username.send_keys(samvad_id)
    password.send_keys(samvad_pw)

    login_page_title = browser.title

    browser.find_element_by_id('btnLoginSubmit').click()

    time.sleep(5)

    main_page_title = browser.title

    if main_page_title == 'Home | SAMV@D':
        #print(main_page_title)
        print("Successfully logged in!")
        return browser
    else:
        print(browser.title)
        print("Failed to login. Returning.")


def browse_search(browser):

    online_articles = None
    print("Browse: Browsing to the search tab and searching for articles in the given date range.")
    browser.get('https://samvad.media/collectionSearch')

    time.sleep(5)
    #print(browser.title)

    #Go to specific date range
    dropdown = browser.find_element_by_class_name('dropdown-form')
    dropdown.click()

    yesterday = (date.today() - timedelta(days=1)).strftime('%d-%m-%Y')

    start_date = browser.find_element_by_id("dateFrom")
    start_date.clear()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
    start_date.send_keys(yesterday)

    end_date = browser.find_element_by_id("dateTo")
    end_date.clear()
    end_date.send_keys(yesterday)

    browser.find_element_by_css_selector('.query-btn > a:nth-child(1)').click()

    time.sleep(5)

    #Select only online articles
    checkbox = browser.find_element_by_css_selector('#facetMedia > li:nth-child(1) > a:nth-child(1) > input:nth-child(1)')
    if checkbox.get_property('name') == 'Online':
        print("Browse: Found online articles in the given date range. Selecting only them..")
        online_articles = True
        checkbox.click()
        shortlist = browser.find_element_by_css_selector('.btn-outline-secondary')
        shortlist.click()
        time.sleep(5)
    else:
        print("Browse: No online articles for the given date range. Returning.")
        online_articles = False

    return browser, online_articles

def browse_download_pdf(browser, download_dir):
    pdf_file = None
    browser.find_element_by_css_selector('button.btn-info').click() #Click on dropdown menu
    pdf_all = browser.find_element_by_css_selector('ul.show > li:nth-child(1) > a:nth-child(1)')
    print("Browse: Attempting to download the pdf file with selected articles.")
    pdf_all.click()

    time.sleep(10)

    old_filename = max([f for f in os.listdir(download_dir)], key=os.path.getctime)
#    print("Browse: Found the latest file in the folder as: ", old_filename)
#    print(date.fromtimestamp(os.path.getmtime(old_filename)))

    if str(old_filename).endswith('.pdf') and date.fromtimestamp(os.path.getmtime(old_filename)) == date.today():
        print("Browse: Downloaded file with name: ", old_filename)

        new_name = 'Online Articles- ' + date.today().strftime("%d %B")
        if not os.path.exists(download_dir+'Online Articles'):
            os.makedirs(download_dir+'Online Articles')
        new_filename = download_dir+ 'Online Articles/' + new_name
        os.rename(old_filename, new_filename)
        print("Browse: Renamed file as: ", new_filename)
        pdf_file = new_filename
    else:
        print("Browse: Failed to download file. Returning.")
        pdf_file = False

    browser.find_element_by_css_selector('button.btn-info').click() #Closing the dropdown
    return browser, pdf_file

def browse_download_csv(browser, download_dir):
    browser.find_element_by_css_selector('button.btn-info').click() #Click on dropdown menu
    csv_all = browser.find_element_by_css_selector('ul.show > li:nth-child(2) > a:nth-child(1)')
    print("Browse: Attempting to download the csv file with selected articles.")
    csv_all.click()

    time.sleep(10)

    old_filename = max([f for f in os.listdir(download_dir)], key=os.path.getctime)
#    print(old_filename)
#    print(date.fromtimestamp(os.path.getmtime(old_filename)))

    if str(old_filename).endswith('.xlsx') and date.fromtimestamp(os.path.getmtime(old_filename)) == date.today():
        print("Browse: Downloaded file with name: ", old_filename)

        new_name = 'Online Articles- ' + date.today().strftime("%d %B") + '.xlsx'
        if not os.path.exists(download_dir+'Online Repo'):
            os.makedirs(download_dir+'Online Repo')
        new_filename = download_dir+ 'Online Repo/' + new_name
        os.rename(old_filename, new_filename)
        print("Browse: Renamed file as: ", new_filename)

        browser.close()
        return new_filename
    else:
        print("Browse: Failed to download file. Returning.")
        browser.close()
        return False
