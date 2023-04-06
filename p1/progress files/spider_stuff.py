# Author: Zack Jaffe-Notier
# Date: 5/13/2020
# Description: building a basic spider

# scraping modules
import scrapy
from scrapy.crawler import CrawlerProcess

# time delay for requests
import time

class MyFirstSpider(scrapy.Spider):
    name = "bgg_spider"

    def start_requests(self):
        urls = ['https://boardgamegeek.com/browse/boardgame/page/']
        for url in urls:
            yield scrapy.Request( url = url, callback = self.parse)

    def parse(self, response):
        html_file = 'bgg.html'
        with open(html_file, 'wb') as fout:
            fout.write(response.body)
