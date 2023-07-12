from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException

from webdriver_manager.chrome import ChromeDriverManager

from bs4 import BeautifulSoup as BS
from urllib.parse import urlparse, parse_qs
from datetime import datetime

import pandas as pd
import numpy as np
import time
import requests
import pyperclip


def naverCafeSearchCrawling(NAVER_ID, NAVER_PW, CAFENAME, NICKNAME, keyword, COMMENTS):
    def css_finds(css_selector):
        return browser.find_elements(By.CSS_SELECTOR, css_selector)

    def css_find(css_selector):
        return browser.find_element(By.CSS_SELECTOR, css_selector)

    def finds_xpath(xpath):
        return browser.find_elements(By.XPATH, xpath)

    def find_xpath(xpath):
        return browser.find_element(By.XPATH, xpath)

    def find_id(id_x):
        return browser.find_element(By.ID, id_x)

    def find_classname(class_name):
        return browser.find_element(By.CLASS_NAME, class_name)

    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('no-sandox')
    options.add_argument('--disable-dev-shm-usage')
    # options.add_argument('--start-maximized')
    options.add_argument("--window-size=1080,800")
    options.add_argument('incognito')

    # service = Service(ChromeDriverManager().install())
    
    # browser = webdriver.Chrome(service=service, options=options)  
    chrome_service = Service('chromedriver')
    chrome_service = Service(executable_path="chromedriver.exe")
    browser = webdriver.Chrome(service = chrome_service, options=options)
    browser.implicitly_wait(3)
    
    # def 1
    browser.get("https://nid.naver.com/nidlogin.login")
    browser.implicitly_wait(2)

    input_id = find_id('id')
    input_pw = find_id('pw')

    time.sleep(2)

    pyperclip.copy(NAVER_ID)
    input_id.send_keys(Keys.CONTROL, "v")

    pyperclip.copy(NAVER_PW) 
    input_pw.send_keys(Keys.CONTROL, "v")
    input_pw.send_keys("\n")

    # Not needed when it's headless
    try:
        no_save_btn = find_id('new.dontsave')
        no_save_btn.click()
    except NoSuchElementException:
        pass

    time.sleep(1)
    
    # def 2
    browser.get(f"https://cafe.naver.com/{CAFENAME}")
    time.sleep(3)
    
    search_input = find_id('topLayerQueryInput')

    pyperclip.copy(keyword)
    search_input.send_keys(Keys.CONTROL, 'v')
    search_input.send_keys('\n')
    
    browser.switch_to.frame("cafe_main")
    time.sleep(2)
    
    find_xpath('//*[@id="currentSearchByTop"]').click()
    time.sleep(1)
    
    find_xpath('//*[@id="sl_general"]/li[2]/a').click()
    find_xpath('//*[@id="main-area"]/div[1]/div[1]/form/div[4]/button').click()
    
    find_xpath('//*[@id="listSizeSelectDiv"]/a').click()
    find_xpath('//*[@id="listSizeSelectDiv"]/ul/li[7]/a').click()
    
    page_numbers_btn = css_finds('div.prev-next > a')
    
    page_nums = []
    for i in page_numbers_btn:
        page_nums.append(i.text)
        
    final_hrefs = []

    if len(page_nums) > 1:
        for i in range(1, 3):
            if i != 1: 
                browser.find_element(By.LINK_TEXT, f"{i}").click()

            soup = BS(browser.page_source, "html.parser")
            soup = soup.find_all(class_='article-board m-tcol-c')[1]

            a_hrefs = soup.find_all("a")

            # def 3
            post_hrefs = []
            for href in a_hrefs:
                if keyword in href.text:
                    post_hrefs.append(href["href"])

            for href in post_hrefs:
                if (href == '#'):
                    pass
                else:
                    parsed_url = urlparse(href)
                    query_params = parse_qs(parsed_url.query)
                    article_id = query_params['articleid'][0]
                    club_id = query_params['clubid'][0]
                    new_url = f"https://cafe.naver.com/{CAFENAME}?iframe_url_utf8=%2FArticleRead.nhn%253Fclubid%3D{club_id}%2526page%3D1%2526boardtype%3DL%2526articleid%3D{article_id}%2526referrerAllArticles%3Dtrue"

                    final_hrefs.append(new_url)

    else:
        soup = BS(browser.page_source, "html.parser")
        soup = soup.find_all(class_='article-board m-tcol-c')[1]

        a_hrefs = soup.find_all("a")

        # def 3
        post_hrefs = []
        for href in a_hrefs:
            if keyword in href.text:
                post_hrefs.append(href["href"])

        for href in post_hrefs:
            if (href == '#'):
                pass
            else:
                parsed_url = urlparse(href)
                query_params = parse_qs(parsed_url.query)
                article_id = query_params['articleid'][0]
                club_id = query_params['clubid'][0]
                new_url = f"https://cafe.naver.com/{CAFENAME}?iframe_url_utf8=%2FArticleRead.nhn%253Fclubid%3D{club_id}%2526page%3D1%2526boardtype%3DL%2526articleid%3D{article_id}%2526referrerAllArticles%3Dtrue"

                final_hrefs.append(new_url)
                
    cmtnicks = []
    cmt_urls = []
    
    for p_href in final_hrefs:
        browser.get(p_href)
        time.sleep(1)
        browser.switch_to.frame("cafe_main")
        time.sleep(1)
        cmtnicks.clear()

        try:
    #         nicksname = browser.find_element(By.CLASS_NAME, 'comment_inbox_name').text
            nickname = NICKNAME
            cmtNicks = browser.find_elements(By.CLASS_NAME, 'comment_nickname')

            if cmtNicks:
                for cmtNick in cmtNicks:
                    cmtnick = cmtNick.text
                    cmtnicks.append(cmtnick)

                if nickname in cmtnicks:
                    continue
                else:
                    time.sleep(1)
                    text_area = browser.find_element(By.CLASS_NAME, 'comment_inbox_text')
                    text_area.click()

                    pyperclip.copy(COMMENTS) 
                    text_area.send_keys(Keys.CONTROL, "v")
                    register_btn = browser.find_element(By.CLASS_NAME, 'btn_register')
                    register_btn.click()
                    
                    cmt_urls.append(browser.current_url)
                    time.sleep(2)
            else:
                time.sleep(1)
                text_area = browser.find_element(By.CLASS_NAME, 'comment_inbox_text')
                text_area.click()

                pyperclip.copy(COMMENTS) 
                text_area.send_keys(Keys.CONTROL, "v")
                register_btn = browser.find_element(By.CLASS_NAME, 'btn_register')
                register_btn.click()
                
                cmt_urls.append(browser.current_url)
                time.sleep(2)

        except NoSuchElementException:
            pass
        
    browser.close()
    
    dt = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    if not cmt_urls:
        pass
    else:
        df = pd.DataFrame({'댓글 URL' : cmt_urls})
        df.to_excel(f'{CAFENAME}_{dt}_1.xlsx', index=False)
        
    return cmt_urls