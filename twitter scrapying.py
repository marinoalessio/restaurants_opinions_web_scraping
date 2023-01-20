from math import fabs
import time
import datetime
from xml.etree.ElementTree import Comment
from hyperlink import URL
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



def Twitter_Crawler(driver, Keyword_Path, Stop_num, kw_start_point=0, save_path=None, start_date=None, end_date=None,
                    limit_language='all'):
    '''
    core function
    :param driver: Chrome Driver
    :param Keyword_Path:the file directory of your keywords which should be csv
    :param Stop_num: the number of the items need to be collect
    :param kw_start_point:start of your keyword
    :param save_path: the file directory of your data which should be csv
    :param start_date: the start date of search
    :param end_date: the end date of search
    :return:
    '''
    df = pd.read_csv(Keyword_Path, encoding='GB18030')
    page_index = 1
    search_end = False
    for index, kw in enumerate(df['keywords']):
        if (index >= kw_start_point):
            Data_List = []
            History_data = []
            url = 'https://twitter.com/search?q=%s&src=typed_query&f=live' % kw
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

                            # get name
                            name = div.find(
                                'span', {'class': 'css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0'}).get_text()
                            # get username
                            user_name = div.find(
                                'div', {'class': 'css-1dbjc4n r-18u37iz r-1wbh5a2 r-13hce6t'}).get_text()
                            # time
                            date = div.find('time')
                            date = date['datetime']
                            date = date.split('T')[0]
                           #timeline
                            if (date > start_date):
                                continue
                            if (date < end_date):
                               search_end = True
                               print('时间超出%s，搜索结束!' % end_date)
                            # comment ,like ,retweet
                            temp = div.find_all('span', {
                                'class': 'css-901oao css-16my406 r-poiln3 r-n6v787 r-1cwl3u0 r-1k6nrdp r-1e081e0 r-qvutc0'})
                            interactionDatas = []
                            for span in temp:
                                interactionDatas.append(span.get_text())
                            try:
                                language = content.get('lang')
                            except:
                                language = 'unknown'
                            # dataSet
                            if ((language == limit_language or limit_language=='all' ) and (str_content not in History_data)):
                                data_list.append(name)  # name
                                data_list.append(user_name)  # user name
                                data_list.append(date)
                                data_list.append(str(str_content).strip().replace('\n', ''))  # content
                                for interactionData in interactionDatas:
                                    data_list.append(interactionData)
                                data_list.append(language)
                                History_data.append(str_content)
                            else:
                                continue
                            Data_List.append(data_list)
                        except:
                            continue
            except Exception as e:
                print(e)
            SaveToCSV(Data_List, index, df, page_index, save_path)


def SaveToCSV(Data_List, index, keyword_df, page_index, save_path):
    '''
    save date in csv
    '''
    df_Sheet = pd.DataFrame(Data_List, columns=['Name', 'User_name', 'Date', 'Content', 'Comments', 'Forward', 'Like', 'language',])
    TIMEFORMAT = '%y%m%d-%H%M%S'
    now = datetime.datetime.now().strftime(TIMEFORMAT)
    kw = keyword_df['keywords'][index]
    #kw = kw.split(' ')[0]
    df_Sheet['Restaurant'] = kw
    csv_path = save_path + '/kw=%s-%s.csv' % (kw, now)
    df_Sheet.to_csv(csv_path, encoding='utf_8_sig')
    print('Already get all information of  {} URL'.format(page_index))
    try:
        print("total %s data" % len(Data_List))
    except:
        print('error')



def Chrome_Config(Chrome_path):
    options = ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)
    # options.add_argument("--headless")  # => headless of chrome
    # options.add_argument("--headless")

    driver = webdriver.Chrome(Chrome_path, options=options)
    return driver


if __name__ == '__main__':

    Chrome_path = '/usr/local/bin/chromedriver' # Enter your chrome driver path here
    driver = Chrome_Config(Chrome_path)  # In this function, you can config your chrome driver
    print('------------------------------------------------------------------------')
    # --------------------------------------------------------------------------------
    # parameters
    Keyword_Path = 'keyword.csv'
    Stop_num = 1000  # this is the number of the items you want to crawl
    kw_start_point = 0  # this parameter decides the start keyword of the crawler.its default value is 0
    save_path = 'data'  # this is the path where you want to save the crawled data
    start_date = '2023-01-01'  # this parameter decides the start date of the crawler.its default value is 2021-01-01
    end_date = '2015-01-01'  # this parameter decides the end date of the crawler.its default value is 2020-01-01
    limit_language = 'all'  # this parameter decides the language of the crawler.its default value is en
    # ----------------------------------------------------------------------------------
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    Twitter_Crawler(driver, Keyword_Path, Stop_num, kw_start_point, save_path, start_date, end_date, limit_language)
    print('------------------------------------------------------------------------')
    driver.close()
