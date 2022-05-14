#to run, write in terminal -> scrapy crawl allhomes -o output.xlsx

#import packages
import scrapy
from bs4 import BeautifulSoup

#start url and allowed domains
class AllhomesSpider(scrapy.Spider):
    name = 'allhomes'
    allowed_domains = ['otodom.pl']
    start_urls = ['https://www.otodom.pl/pl/oferty/sprzedaz/mieszkanie/mazowieckie?page=1']

#find each property box with information needed
    def parse(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        content = soup.find_all('li', {'class': 'css-p74l73 es62z2j17'})
        pass

#for each property, scrape the title, location, and price of the listing
        for property in content:
            yield {
                'name': property.find('h3').text,
                'location': property.find('span', {'class': 'css-17o293g es62z2j9'}).text,
                'price': property.find('span', {'class': 'css-rmqm02 eclomwz0'}).text
            }
#for loop to update the "next page" by adding ending of pages 2-100,
# then call the parse function again for each next page
        for x in range(2,101):
            next_page = 'https://www.otodom.pl/pl/oferty/sprzedaz/mieszkanie/mazowieckie?page=' + str(x)
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

