#!/usr/bin/env python
# coding: utf-8

import sys
import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
import time
import re
import pandas as pd

def get_reviews_from_url(url):
    
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
    driver.get(url)
    
    num_page = 15 # max number of pages to scrape
    df = pd.DataFrame(columns=['title', 'date', 'rating', 'review'])
    
    for i in range(0, num_page):
    
        time.sleep(2)
        element = driver.find_element(By.XPATH, "//span[@class='taLnk ulBlueLinks']") # expand the review 
        driver.execute_script("arguments[0].click();", element)
        time.sleep(2)

        container = driver.find_elements(By.XPATH, ".//div[@class='review-container']")

        for j in range(len(container)):

            title = container[j].find_element(By.XPATH, ".//span[@class='noQuotes']").text
            date = container[j].find_element(By.XPATH, ".//span[contains(@class, 'ratingDate')]").get_attribute("title")
            rating = container[j].find_element(By.XPATH, ".//span[contains(@class, 'ui_bubble_rating bubble_')]").get_attribute("class").split("_")[3]
            review = container[j].find_element(By.XPATH, ".//p[@class='partial_entry']").text.replace("\n", " ")
        
            row = {'title':title, 'date':date, 'rating':rating, 'review':review}
            df = df.append(row, ignore_index=True)

        if (driver.find_elements(By.XPATH, ".//a[@class='nav next ui_button primary disabled']")):
            break # if there are no pages left, constraint: pages <= num_pages
        
        # change the page
        next = driver.find_element(By.XPATH, './/a[@class="nav next ui_button primary"]')
        driver.execute_script("arguments[0].click();", next)
        time.sleep(2)

    return df
    driver.close()
