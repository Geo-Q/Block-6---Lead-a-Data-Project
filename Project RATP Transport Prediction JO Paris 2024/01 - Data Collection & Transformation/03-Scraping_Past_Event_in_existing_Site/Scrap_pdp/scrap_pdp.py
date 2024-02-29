import os
import logging
import scrapy
from scrapy.crawler import CrawlerProcess
import pandas as pd


class PdpSpider(scrapy.Spider):

    name = "pdp"

    start_urls = [
        'https://www.transfermarkt.fr/paris-saint-germain/spielplandatum/verein/583/plus/0?saison_id=&wettbewerb_id=&day=&heim_gast=heim&punkte=&datum_von=01.01.2015&datum_bis=31.12.2022',
    ]


    def parse(self, response):
        events = response.xpath('/html/body/div[2]/main/div[2]/div[1]/div[1]/div[3]/table/tbody/tr')
        for event in events:
            yield {
                "date": event.xpath('td[2]/text()').get()
                ,
                "place": event.xpath('td[4]/text()').get()
                ,
                "affluence": event.xpath('td[9]/text()').get()
            }


# Name of the file where the results will be saved
filename = "past_events_pdp.json"

# If file already exists, delete it before crawling (because Scrapy will
# concatenate the last and new results otherwise)
if filename in os.listdir('src/'):
        os.remove('src/' + filename)

# Declare a new CrawlerProcess with some settings
## USER_AGENT => Simulates a browser on an OS
## LOG_LEVEL => Minimal Level of Log
## FEEDS => Where the file will be stored
## More info on built-in settings => https://docs.scrapy.org/en/latest/topics/settings.html?highlight=settings#settings
process = CrawlerProcess(settings = {
    'USER_AGENT': 'Chrome/116.0.0.0',
    'LOG_LEVEL': logging.INFO,
    'DOWNLOAD_DELAY': 5,
    "AUTOTHROTTLE_ENABLED": True,
    "COOKIES_ENABLED": False,
    "FEEDS": {
        'src/' + filename: {"format": "json"},
    }
})

# Start the crawling using the spider you defined above
process.crawl(PdpSpider)
process.start()

