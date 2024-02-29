import os
import logging
import scrapy
from scrapy.crawler import CrawlerProcess
import pandas as pd


class YelpSpider(scrapy.Spider):

    name = "sdf"

    start_urls = [
        'https://www.stadefrance.com/fr/billetterie/archives?field_date_closing_event_value=now&year=all',
    ]


    def parse(self, response):
        events = response.xpath('/html/body/div/div/div/div/div/main/div/div/div/div/div/div/div/div')
        for event in events:
            yield {
                "event_name": event.xpath('div[2]/div[1]/div[1]/text()').get()
                ,
                "date": event.xpath('div[3]/span[1]/text()').get()
                ,
                "event_description": event.xpath('div[2]/div[1]/div[2]/text()').get()
            }

# Name of the file where the results will be saved
filename = "past_events_sdf.json"

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
process.crawl(YelpSpider)
process.start()

