from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUi
import sys
from threading import Thread
import qdarktheme
from selenium.webdriver.common.by import By
import os
import time
import concurrent.futures
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
from bs4 import BeautifulSoup
import re
import requests
from faker import Faker
import colorama
from colorama import Fore
from colorama import init
from openpyxl import Workbook
from selenium.webdriver.common.action_chains import ActionChains
from termcolor import colored
from fake_useragent import UserAgent
job_id = 0


def find(query, emails, method, jobs, user):
    job = jobs(name=query, status="pending", user=user,
               emails="Extracting Emails....please wait!", progress="0")
    job.save()

    # random user agent string
    ua = UserAgent()
    user_agent = ua.random
    print(user_agent)

    p = 0
    emailsToScrape = int(emails)
    emailScraped = 0
    scrapeMethod = method  # ? also can be b2c or both
    keyword = query
    scrapedEmails = ""

    # ? input  then no of times of searches
    if (scrapeMethod == "b2c"):
        keyword = f""""{keyword}" site:facebook.com "@gmail.com" OR "@yahoo.com" OR "@outlook.com" """
    elif (scrapeMethod == "b2b"):
        keyword = f""""{keyword}" site:facebook.com Email " * @ * .com OR .org OR .net OR .io" -gmail -hotmail -outlook -yahoo"""
    else:
        keyword = f""""{keyword}" site:facebook.com Email " * @ * .com OR .org OR .net OR .io" """

    # ? chrome options
    options = Options()
    options.add_argument('start-maximized')
    # options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    # options.add_argument(f'user-agent={user_agent}')
    options.add_experimental_option('debuggerAddress', '127.0.0.1:9222')
    driver = webdriver.Chrome(service=Service(
        ChromeDriverManager().install()), options=options)

    # ? setting to show 100 results per page
    # driver.get('https://www.google.com/preferences?hl=en&prev=https://www.google.com/search?q%3Dheadless%2Band%2Bno%2Bsandbox%2Bin%2Bpython%2Bselenium%26rlz%3D1C1CHBD_enPK1046PK1046%26oq%3Dheadless%2Band%2Bno%2Bsandbox%2Bin%2Bpython%2Bselenim%26aqs%3Dchrome.1.69i57j33i10i160l3.19759j0j7%26sourceid%3Dchrome%26ie%3DUTF-8%26start%3D0%26num%3D50')
    # script = """
    #     arguments[0].setAttribute('style',"left:342px;")
    #     arguments[1].setAttribute('aria-value-now',"100")
    #     arguments[2].setAttribute('value',"100")
    #     """
    # time.sleep(3)
    # driver.execute_script(script, driver.find_element(
    #     by=By.CLASS_NAME, value="goog-slider-thumb"), driver.find_element(
    #     by=By.CLASS_NAME, value="goog-slider"), driver.find_element(
    #     by=By.NAME, value="num"))
    # time.sleep(2)
    # driver.find_element(by=By.CLASS_NAME, value="jfk-button-action").click()
    # time.sleep(3)

    # ? start scraping
    driver.get('https://www.google.com')
    time.sleep(3)
    input = driver.find_element(by=By.NAME, value='q')
    input.clear()
    input.send_keys(keyword)
    input.send_keys(Keys.ENTER)
    urls = []

    current = 1
    total = len(driver.find_elements(by=By.CLASS_NAME, value="fl"))+1
    while (True):
        # ? finding resulting Links
        print('Extracting the page...')
        url = driver.current_url
        print(url)
        p = (current/total)*100
        print(f'Scraping {url}')
        text = """"""
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        for i in soup.find_all():
            text += i.text

        # ? extracting emails from text
        pattrn = r'[\w.+\_]+@[\w-]+\.com'
        emails = re.findall(pattrn, text)
        emails = list(
            set([email for email in emails if (not (str(email)[0].isdigit()))]))

        # ? printing emails
        for email in enumerate(emails):
            print(email[1])
            scrapedEmails = scrapedEmails+f"{email[1]} \n"

        emailScraped = emailScraped+len(emails)
        # check if required emails are met
        if (emailsToScrape <= emailScraped):
            break

        try:
            driver.find_element(by=By.ID, value="pnnext").click()
        except:
            break
        print(f'{int(p)} % ')     # showing percentage
        job_id = job.id
        ujob = jobs.objects.get(id=job.id)
        ujob.progress = str(p)          # saving progress in backend
        ujob.emails = str(scrapedEmails)  # saving emails in backend
        ujob.save()

        time.sleep(3)
        current = current+1

    ujob = jobs.objects.get(id=job.id)
    ujob.progress = str(100)
    ujob.status = "completed"
    ujob.save()

    print('Scraping Done 100%')
    return scrapedEmails
