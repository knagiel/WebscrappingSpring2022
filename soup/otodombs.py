#import the packages needed
import requests
from bs4 import BeautifulSoup
import time
import pandas as pd


#list to be used to store the information
mazowieckie_for_sale = []

#for loop below to add an ending number to the url which will result in scraping 100 pages.
#This will start with page 1 of information and end on page 100 of the results
for x in range(1, 101):
    url = 'https://www.otodom.pl/pl/oferty/sprzedaz/mieszkanie/mazowieckie?page='
    r = requests.get(url+str(x))

    soup = BeautifulSoup(r.content, 'html.parser')
    #content variable finds each "box" containing information for each listing
    content = soup.find_all('li', class_='css-p74l73 es62z2j17')

    #for loop then loops through each property content "box" and finds the title, location, and price
    for property in content:
        name = property.find('h3').text
        location = property.find('span', class_='css-17o293g es62z2j9').text
        price = property.find('span', class_='css-rmqm02 eclomwz0').text

        property_specs = {  #add information to dictionary
            'name': name,
            'location': location,
            'price': price
        }

        mazowieckie_for_sale.append(property_specs) #append to list
    time.sleep(2) #sleep 2 seconds between each request

#add to dataframe, print the head of dataframe, and export to excel
df = pd.DataFrame(mazowieckie_for_sale)
print(df.head())
df.to_excel('mazowieckie_for_sale.xlsx')
