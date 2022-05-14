from selenium import webdriver
from selenium.common import exceptions
import pandas as pd
from selenium.webdriver.common.by import By


driver = webdriver.Chrome()
url = 'https://www.otodom.pl/pl/oferty/sprzedaz/mieszkanie/mazowieckie?page='
driver.get(url)

infos = driver.find_elements(By.CLASS_NAME, 'css-14cy79a e3x1uf06')

for info in infos:
    title = info.find_elements(By.XPATH, './/*[@id="__next"]/div[2]/main/div[1]/div[3]/div[1]/div[2]/div[2]/ul/li[1]/a/article/div[1]/h3').text
    price = info.find_elements(By.XPATH, './/*[@id="__next"]/div[2]/main/div[1]/div[3]/div[1]/div[2]/div[2]/ul/li[1]/a/article/div[2]/span[1]').text
    location = info.find_elements(By.XPATH, './/*[@id="__next"]/div[2]/main/div[1]/div[3]/div[1]/div[2]/div[2]/ul/li[1]/a/article/p/span').text
    print(title, price, location)

title_list = []
price_list = []
location_list = []

i = 0
while i < 100:
    try:
        apartment_info = driver.find_element(By.CLASS_NAME, 'css-14cy79a e3x1uf06')

        for info in infos:
            title = info.find_elements(By.XPATH, './/*[@id="__next"]/div[2]/main/div[1]/div[3]/div[1]/div[2]/div[2]/ul/li[1]/a/article/div[1]/h3').text
            price = info.find_elements(By.XPATH, './/*[@id="__next"]/div[2]/main/div[1]/div[3]/div[1]/div[2]/div[2]/ul/li[1]/a/article/div[2]/span[1]').text
            location = info.find_elements(By.XPATH, './/*[@id="__next"]/div[2]/main/div[1]/div[3]/div[1]/div[2]/div[2]/ul/li[1]/a/article/p/span').text
            print(title, price, location)

            title_list.append(title)
            price_list.append(price)
            location_list.append(location)

        driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/main/div[1]/div[3]/div[1]/div[4]/div/nav/button[6]').click()
        i += 1

    except exceptions.StaleElementReferenceException:
        pass

df = pd.DataFrame(list(zip(title_list, price_list, location_list)), columns=['name', 'location', 'price'])

homes_for_sale = df.to_csv('mazowieckie_for_sale.csv', index=False)
