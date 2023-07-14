from subprocess import CREATE_NO_WINDOW
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import *

from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup as BS
from datetime import datetime

import pandas as pd
import time
import pyperclip
import os


def find_css(css_selector, browser):
    return browser.find_element(By.CSS_SELECTOR, css_selector)

def finds_css(css_selector, browser):
    return browser.find_elements(By.CSS_SELECTOR, css_selector)

def find_xpath(xpath, browser):
    return browser.find_element(By.XPATH, xpath)

def finds_xpath(xpath, browser):
    return browser.find_elements(By.XPATH, xpath)

def find_id(e_id, browser):
    return browser.find_element(By.ID, e_id)

def find_className(cn, browser):
    return browser.find_element(By.CLASS_NAME, cn)

def finds_className(cn , browser):
    return browser.find_elements(By.CLASS_NAME, cn)

def find_linktext(lt, browser):
    return browser.find_element(By.LINK_TEXT, lt)

COUNT = 50

def open_browser():
    options = webdriver.ChromeOptions()
    options.add_argument('--no--sandbox')
    options.add_argument('no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1080,800')
    options.add_argument('incognito')

    chrome_service = Service('chromedriver')
    chrome_service.creationflags = CREATE_NO_WINDOW
    chrome_service = Service(executable_path="chromedriver.exe")
    browser = webdriver.Chrome(service=chrome_service, options=options)

    browser.get("https://nid.naver.com/nidlogin.login")
    browser.implicitly_wait(2)
    
    return browser

def login(browser, NAVER_ID, NAVER_PW):
    input_id = find_id('id', browser)
    input_pw = find_id('pw', browser)

    time.sleep(2)

    pyperclip.copy(NAVER_ID)
    input_id.send_keys(Keys.CONTROL, "v")

    pyperclip.copy(NAVER_PW) 
    input_pw.send_keys(Keys.CONTROL, "v")
    input_pw.send_keys("\n")

    try:
        no_save_btn = find_id('new.dontsave', browser)
        no_save_btn.click()
    except NoSuchElementException:
        pass

def top_to_bottom(browser):
    last_height = browser.execute_script("return document.body.scrollHeight")

    while True:
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        time.sleep(.5)
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight-50);")
        time.sleep(.5)

        new_height = browser.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            break

        last_height = new_height

def setSearch(browser, kw):
    browser.get('https://www.naver.com/')
    search_input = find_id('query', browser)

    time.sleep(1)

    pyperclip.copy(kw)
    search_input.send_keys(Keys.CONTROL, 'v')
    search_input.send_keys('\n')

    time.sleep(2)

    find_linktext('VIEW', browser).click()

    time.sleep(1.5)

    find_linktext('블로그', browser).click()

    time.sleep(.5)

def get_urls(browser):
    unique_urls = []
    unique_id = []
    final_hrefs = []
    names = []
    
    soup = BS(browser.page_source, "html.parser")
    a_hrefs = soup.find_all(class_ = "total_tit")

    for href in a_hrefs:
        final_hrefs.append(href['href'])

    final_hrefs = list(set(final_hrefs))


    for url in final_hrefs:
        id_ = url.split('.com/')[-1].split('/')[0]
        names.append(id_)
        if id_ not in unique_id:
            unique_id.append(id_)


    for id_ in unique_id:
        count = 0
        for url in final_hrefs:
            if id_ in url:
                count += 1
                if count == 1:
                    unique_urls.append(url)
                else:
                    break
                    
    return unique_urls

def writeCmt(browser, KW, cmt):
    cmtNicks = []
    cmt_write_urls = []
    error_urls = []
    
    for i in KW:
        setSearch(browser, i)
        cmtNicks.clear()
        cmt_write_urls.clear()

        top_to_bottom(browser)

        unique_urls = get_urls(browser)
        try:
            for href in unique_urls:
                print(len(cmt_write_urls))
                if len(cmt_write_urls) >= COUNT:
                    break
                cmtNicks.clear()
                try:
                    browser.get(href)
                    time.sleep(.5)

                    try:
                        browser.switch_to.frame("mainFrame")
                        time.sleep(1)
                    except: pass

                    a_test = find_css('div.area_comment.pcol2 > a', browser)
                    browser.execute_script("arguments[0].click();", a_test)
                    time.sleep(2)

                    nicknames = finds_className('u_cbox_nick', browser)
                    my_nickname = find_className('u_cbox_write_name', browser).text
                    print(my_nickname)

                    if nicknames:
                        for nc in nicknames:
                            cmtNicks.append(nc.text)

                        if my_nickname in cmtNicks:
                            continue
                        else:
                            time.sleep(1)
                            cmt_textarea = find_className('u_cbox_text_mention', browser)

                            cmt_textarea.send_keys(' ')

                            pyperclip.copy(cmt)
                            cmt_textarea.send_keys(Keys.CONTROL, 'v')

                            time.sleep(1)

                            commit_btn = find_css('div.u_cbox_upload > button.u_cbox_btn_upload', browser)
                            commit_btn.click()
                            print(browser.current_url)
                            cmt_write_urls.append(browser.current_url)
                            time.sleep(3)
                    else:
                        time.sleep(1)
                        cmt_textarea = find_className('u_cbox_text_mention', browser)

                        cmt_textarea.send_keys(' ')

                        pyperclip.copy(cmt)
                        cmt_textarea.send_keys(Keys.CONTROL, 'v')

                        time.sleep(1)

                        commit_btn = find_css('div.u_cbox_upload > button.u_cbox_btn_upload', browser)
                        commit_btn.click()
                        print(browser.current_url)
                        cmt_write_urls.append(browser.current_url)
                        
                        screenshot_folder = 'screenshot/'
                        start_num = 1
                        
                        if not os.path.exists(screenshot_folder):
                            os.makedirs(screenshot_folder)
                            
                        esisting_files = os.listdir(screenshot_folder)
                        screenshot_num = start_num + len(esisting_files)
                        
                        screenshot_path = f'{screenshot_folder}screenshot_{screenshot_num}.png'
                        browser.save_screenshot(screenshot_path)
                        
                        time.sleep(3)

                except :
                    error_urls.append(browser.current_url)
                    pass
        except:
            dt = datetime.now().strftime("%Y-%m-%d_%H%M%S")

            df = pd.DataFrame({"작성한 URL" : cmt_write_urls})
            df.to_excel(f"{dt}_{i}.xlsx")

        
        dt = datetime.now().strftime("%Y-%m-%d_%H%M%S")

        df = pd.DataFrame({"작성한 URL" : cmt_write_urls})
        df.to_excel(f"{dt}_{i}.xlsx")

    return cmt_write_urls

def start_function(NAVER_ID, NAVER_PW, KW, cmt):

    browser = open_browser()
    
    login(browser, NAVER_ID, NAVER_PW)

    cmt_write_urls  =  writeCmt(browser, KW, cmt)


    return cmt_write_urls