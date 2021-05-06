# -*- coding: utf-8 -*-
"""
Created on Thu Apr 15 21:33:30 2021

@author: kolom
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from tqdm import tqdm
import re
import pandas as pd

def remove_spaces(string):
    return (re.sub(' ','',string))

opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36 OPR/75.0.3969.149")

driver = webdriver.Chrome('C:/Users/kolom/chromedriver/chromedriver.exe', chrome_options=opts)

pages = 7 #сюда вставлять количество страниц в разделе

pbar = tqdm(total = pages)
links = []
for i in range(1,pages+1):
    page = 'https://lenta.com/catalog/bytovaya-himiya/sredstva-dlya-mytya-posudy/?page={}'.format(i)
    driver.get(page)
    pbar.update(1)
    items = driver.find_elements_by_xpath('/html/body/div[1]/div[1]/div/main/article/div/div/div/div[2]/div/div[5]/div[2]/div[1]/div/div[1]/div[*]/a')

    links.extend([a.get_attribute("href") for a in items])
    time.sleep(1)
pbar.close()

data = []
pbar1 = tqdm(total = len(links))
for link in links:
    item = {}
    driver.get(link)
    name = driver.find_element_by_xpath('/html/body/div[1]/div[1]/div/main/article/div/div/div[2]/div[1]/div[1]/h1').text
    rub_sale = driver.find_element_by_xpath('/html/body/div[1]/div[1]/div/main/article/div/div/div[2]/div[1]/div[3]/div[2]/div[1]/div/div/div[1]/div[2]/div[2]/div[1]/span[1]').text
    penny_sale = driver.find_element_by_xpath('/html/body/div[1]/div[1]/div/main/article/div/div/div[2]/div[1]/div[3]/div[2]/div[1]/div/div/div[1]/div[2]/div[2]/div[1]/small').text
    rub_normal = driver.find_element_by_xpath('/html/body/div[1]/div[1]/div/main/article/div/div/div[2]/div[1]/div[3]/div[2]/div[1]/div/div/div[1]/div[2]/div[1]/div[1]/span[1]').text
    penny_normal = driver.find_element_by_xpath('/html/body/div[1]/div[1]/div/main/article/div/div/div[2]/div[1]/div[3]/div[2]/div[1]/div/div/div[1]/div[2]/div[1]/div[1]/small').text
    item['Название'] = name
    item['Ссылка'] = link
    item['Обычная цена'] = float(remove_spaces(rub_normal))+float(remove_spaces(penny_normal))/100 
    item['Цена по карте'] = float(remove_spaces(rub_sale))+float(remove_spaces(penny_sale))/100
    
    attributes = driver.find_elements_by_class_name('sku-card-tab-params__item')
    for attribute in attributes:
        atr_name = attribute.find_element_by_xpath('dt/label').text
        try:
            atr_value = attribute.find_element_by_xpath('a').text
        except:
            atr_value = attribute.find_element_by_xpath('dd').text
        item[atr_name] = atr_value
    data.append(item)
    pbar1.update(1)
    time.sleep(1)
pbar1.close()

database = pd.DataFrame(data)
database.to_csv('result.csv', index = False, sep = ';', encoding='utf8', decimal = ',')
database.to_excel('result.xlsx', sheet_name='Sheet1', index=False)
