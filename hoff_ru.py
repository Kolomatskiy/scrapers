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

pages = 3 #сюда вставлять количество страниц в разделе

links = []
items = driver.find_elements_by_xpath('//*[@id="Section01"]/div[*]/div[4]/a')
links.extend([a.get_attribute("href") for a in items])
pbar = tqdm(total = pages)
links = []
basepage = 'https://hoff.ru/catalog/tovary_dlya_doma/hoztovary/tovary_dlya_uborki/meshki_dlya_musora/' #сюда вставлять ссылку
for i in range(1,pages+1):
    page = '{}page{}'.format(basepage, i)
    driver.get(page)
    pbar.update(1)
    items = driver.find_elements_by_xpath('//*[@id="Section01"]/div[*]/div[4]/a')
    links.extend([a.get_attribute("href") for a in items])
    time.sleep(0.2)
pbar.close()


data = []
pbar1 = tqdm(total = len(links))
for link in links:
    item = {}
    driver.get(link)
    name = driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div[1]/h1').text.split('#')[0]
    item['Название'] = name
    item['Ссылка'] = link
    articul = driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div[1]/h1').text.split('#')[1]
    item['Артикул'] = articul
    rub_normal = int(remove_spaces(driver.find_element_by_class_name('price-current').text.replace('P','')))
    item['Обычная цена'] = rub_normal
    try:
        rub_sale = int(remove_spaces(driver.find_element_by_class_name('discount-info').find_element_by_xpath('div[1]/span[1]').text))
        item['Акционная цена'] = rub_sale
    except:
        pass
    
    attributes = driver.find_elements_by_class_name('single-param')
    for attribute in attributes:
        atr_name = attribute.find_element_by_xpath('div[1]/span').text.replace(':','')
        try:
            atr_value = attribute.find_element_by_xpath('div[2]/span').text
            item[atr_name] = atr_value
        except:
            pass
    data.append(item)
    pbar1.update(1)
    time.sleep(0.2)
pbar1.close()

database = pd.DataFrame(data)
database.to_csv('result.csv', index = False, sep = ';', encoding='utf8', decimal = ',')
database.to_excel('result.xlsx', sheet_name='Sheet1', index=False)
