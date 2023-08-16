import json
import scrapy
from urllib.parse import urljoin
import re

class FlipkartProduct(scrapy.Spider):
    name = 'flipkart_seller'
    def start_requests(self):
        searchURL = "https://www.flipkart.com/search?q=instant+food&otracker=search&otracker1=search&marketplace=GROCERY&as-show=on&as=off&page=1"
        yield scrapy.Request(url=amazon_search_url, callback=self.discover_product_urls, meta={'page': 1})

    def discover_product_urls(self, response):
        page = response.meta['page']
        search_products = response.css("div._35mN4f")
        
        for product in search_products:
            product_url = product.css("a._1fQZEK::attr(href)").extract_first()
            if product_url:
                absolute_url = urljoin("https://www.flipkart.com/", product_url)
                yield scrapy.Request(url=absolute_url, callback=self.parse_product_data, meta=page)

        # You can continue to the next page if needed
        next_page = response.css('a._1LKTO3::attr(href)').extract_first()
        if next_page:
            next_page_url = urljoin(response.url, next_page)
            yield scrapy.Request(url=next_page_url, callback=self.discover_product_urls, meta={'page': page + 1})

    def parse_product_data(self, response):
        image_data = json.loads(re.findall(r"colorImages':.*'initial':\s*(\[.+?\])},\n", response.text)[0])
        variant_data = re.findall(r'dimensionValuesDisplayData"\s*:\s* ({.+?}),\n', response.text)
        feature_bullets = [bullet.strip() for bullet in response.css("#feature-bullets li ::text").getall()]
        seller_name = []
        price = response.css('.a-price span[aria-hidden="true"] ::text').get("")
        if not price:
            price = response.css('.a-price .a-offscreen ::text').get("")
        yield {
            "name": response.css("#productTitle::text").get("").strip(),
            "price": price,
            "stars": response.css("i[data-hook=average-star-rating] ::text").get("").strip(),
            "rating_count": response.css("div[data-hook=total-review-count] ::text").get("").strip(),
            "feature_bullets": feature_bullets,
            "images": image_data,
            "variant_data": variant_data,
        }