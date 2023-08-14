import json
import scrapy
from urllib.parse import urljoin
import re

class AmazonSellerSpider(scrapy.Spider):
    name = 'amazon_seller'
    dataList = []

    def start_requests(self):
        sellerLink = ["https://www.amazon.in/s?me=A1V6GP6UHBM01Y&marketplaceID=A21TJRUUN4KGV", "https://www.amazon.in/s?me=A1UJGTKG9XY4YH&marketplaceID=A21TJRUUN4KGV", "https://www.amazon.in/s?me=AKTXA7AJ89MBZ&marketplaceID=A21TJRUUN4KGV"]
        for link in sellerLink:
            yield scrapy.Request(url=link, callback=self.product_url, meta={'page':1})

    def product_url(self, response):
        page = response.meta['page']
        search_products = response.css("div.s-result-item[data-component-type=s-search-result]")
        for product in search_products:
            data = {}
            data['producturl'] = product.css("h2>a::attr(href)").get()
            data['productname'] = product.css("h2>a ::text").get()
            data['price'] = product.css('.a-price span[aria-hidden="true"] ::text').get("")
            data['star_rating'] = product.css("i.a-icon.a-icon-star-small.aok-align-bottom[data-hook=average-star-rating] ::text").get("").strip()

            self.dataList.append(data)
    #def closed(self, response):
        #with open('amazon_data.json', 'a') as f:
            #json.dump(self.dataList, f)