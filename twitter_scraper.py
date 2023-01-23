#!/usr/bin/env python
# coding: utf-8

# In[2]:


from math import fabs
import time
import datetime
from xml.etree.ElementTree import Comment
#from hyperlink import URL
from numpy import common_type
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium import webdriver
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import pandas as pd
from selenium.webdriver import ActionChains
from selenium.webdriver import ChromeOptions
import os
from selenium.webdriver import ChromeOptions
import os


# In[138]:


def twitter_scraper(query, Stop_num, kw_start_point=0, start_date=None, end_date=None):
    
    options = webdriver.ChromeOptions()
    options.add_argument('-headless')
    options.add_argument('-no-sandbox')
    options.add_argument('-disable-dev-shm-usage')
    options.add_argument("enable-automation")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-extensions")
    options.add_argument("--dns-prefetch-disable")
    options.add_argument("--disable-gpu")
    page_index = 1
    search_end = False
    
    Data_List = []
    History_data = []
    
    driver = webdriver.Chrome('chromedriver', options = options)
    url = 'https://twitter.com/search?q=%s&src=typed_query&f=live' % query
    driver.get(url)
    driver.implicitly_wait(10)

    try:
        old_scroll_height = 0  # page in the top
        js1 = 'return document.body.scrollHeight'  # get the height of page
        js2 = 'window.scrollTo(0, document.body.scrollHeight)'  # scroll the page
        while ((driver.execute_script(js1) > old_scroll_height and len(
                Data_List) < Stop_num) and search_end == False):  # compare the height with previous page
            
            old_scroll_height = driver.execute_script(js1)  # get height of page
            driver.execute_script(js2)  # scroll page
            time.sleep(3)  # timesleep
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            divs = soup.find_all('div', {'class': 'css-1dbjc4n r-1iusvr4 r-16y2uox r-1777fci r-kzbkwu'})

            for divIndex, div in enumerate(divs):
                data_list = []
                try:
                    content = div.find('div', {
                        'class': 'css-901oao r-18jsvk2 r-37j5jr r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-bnwqim r-qvutc0'})
                    if (content):
                        str_content = content.get_text()
                    else:
                        content = div.find('div', {
                            'class': 'css-901oao r-18jsvk2 r-1tl8opc r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-bnwqim r-qvutc0'})
                        str_content = content.get_text()
                    if (('https://instagram.com' in str_content) and ('oto ' in str_content)):
                        pass
                    
                    # time
                    date = div.find('time')
                    date = date['datetime']
                    date = date.split('T')[0]
                    
                   #timeline
                    if (date > start_date):
                        continue
                    if (date < end_date):
                       search_end = True

                    # dataSet
                    if (str_content not in History_data):
                        data_list.append(date)
                        data_list.append(str(str_content).strip().replace('\n', ''))  # content
                        History_data.append(str_content)
                    else:
                        continue
                        
                except:
                    continue
                    
                Data_List.append(data_list)

    except Exception as e:
        print(e)
        
    df_sheet = pd.DataFrame(Data_List, columns=['Date', 'Content'])
    driver.close()
    return df_sheet


# In[ ]:

Stop_num = 100  # max number of tweets
kw_start_point = 0  # this parameter decides the start keyword of the crawler.its default value is 0
start_date = '2023-01-20'  # this parameter decides the start date of the crawler.its default value is 2021-01-01
end_date = '2015-01-01'  # this parameter decides the end date of the crawler.its default value is 2020-01-01

# To execute
query = ''
df = twitter_scraper(query, Stop_num, kw_start_point, start_date, end_date)
