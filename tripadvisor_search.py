#!/usr/bin/env python
# coding: utf-8

# In[59]:


import sys
import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import re
import pandas as pd


# In[194]:


def get_top_from_query(query, max_elements=10):
    options = webdriver.ChromeOptions()
    options.add_argument('-headless')
    options.add_argument('-no-sandbox')
    options.add_argument('-disable-dev-shm-usage')
    options.add_argument("enable-automation")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-extensions")
    options.add_argument("--dns-prefetch-disable")
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome('chromedriver', options = options)
    
    root = "https://www.tripadvisor.com/"

    url = root + 'Search?q=' + query + " restaurants"
    url = url.replace(' ', '%20')
    driver.get(url)
    html = driver.page_source
    print('Scraping information from this address: ', driver.current_url)
    
    rest_list = driver.find_elements(By.XPATH, "//div[@data-test-target='restaurants-list']/div")

    idx = 0

    df = pd.DataFrame(columns = ['name', 'link'])

    for rest in rest_list:

        if(len(rest.get_attribute("class")) > 0):
            continue
        #img = rest.find_element(By.XPATH, "//ul//div[contains(@style,'background-image')]")
        #img = img.get_attribute("style").replace('background-image: url("', "")
        #img = img.replace('");', "")
        link = rest.find_element(By.TAG_NAME, "a").get_attribute("href")

        match = re.search(r'Reviews-(.+?).html', link)
        name = match.group(1)
        name = name.replace('_', ' ').replace('-', ' ')
        words = name.split()
        name = (" ".join(sorted(set(words), key=words.index))) # remove duplicates

        df = df.append({'name':name,'link':link}, ignore_index=True)

        if(idx >= max_elements-1):
            break
        idx += 1
        
    return df


# In[195]:


get_top_from_query('london', max_elements=10)

