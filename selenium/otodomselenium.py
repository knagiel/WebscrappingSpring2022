# -*- coding: utf-8 -*-
import pandas as pd
import scrapy
from selenium import webdriver
from scrapy.selector import Selector
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
import requests
from bs4 import BeautifulSoup

name = 'dom'  # if you use base of spider but want to scrape other page, you need to update name of the spider
allowed_domains = ['otodom.pl']
start_urls = ['http://otodom.pl/']

driver = webdriver.Chrome()
driver.get('https://www.otodom.pl/pl/oferty/sprzedaz/mieszkanie/mazowieckie?page=1')
sleep(3)

Button = driver.find_element(by=By.XPATH, value='//*[@id="onetrust-accept-btn-handler"]')
Button.click()

title_list = []
price_list = []
location_list = []

def parse(self, response):
    soup = BeautifulSoup(response.text, 'lxml')
    contents = soup.find_all('li', {'class': 'css-p74l73 es62z2j17'})


    for content in contents:
        title = content.find_element(By.XPATH,
                                     '//*[@id="__next"]/div[2]/main/div[1]/div[3]/div[1]/div[2]/div[2]/ul/li[1]/a/article/div[1]/h3').text
        price = content.find_element(By.XPATH,
                                     './/*[@id="__next"]/div[2]/main/div[1]/div[3]/div[1]/div[2]/div[2]/ul/li[1]/a/article/div[2]/span[1]').text
        location = content.find_element(By.XPATH,
                                        './/*[@id="__next"]/div[2]/main/div[1]/div[3]/div[1]/div[2]/div[2]/ul/li[1]/a/article/p/span').text

        title_list.append(title)
        price_list.append(price)
        location_list.append(location)
    
    
    for url in range(2, 101):
        next_page = 'https://www.otodom.pl/pl/oferty/sprzedaz/mieszkanie/mazowieckie?page=' + str(url)
        next_page = response.urljoin(next_page)
        yield scrapy.Request(next_page, callback=self.parse)
        
df = pd.DataFrame(list(zip(title_list, price_list, location_list)), columns=['name', 'location', 'price'])

homes_for_sale = df.to_csv('mazowieckie_for_sale.csv', index=False)
