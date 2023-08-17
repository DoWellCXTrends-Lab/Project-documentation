import json
import scrapy
from urllib.parse import urljoin
import re

class FlipkartProduct(scrapy.Spider):
    name = 'flipkart_seller'
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    def start_requests(self):
        searchURL = "https://www.flipkart.com/search?q=instant+food&otracker=search&otracker1=search&marketplace=GROCERY&as-show=on&as=off&page=1"
        yield scrapy.Request(url=searchURL, callback=self.discover_product_urls, meta={'page': 1}, headers=self.headers)

    def discover_product_urls(self, response):
        page = response.meta['page']
        search_products = response.css("div._35mN4f")
        
        for product in search_products:
            product_url = product.css("div._1vhGDP a::attr(href)").extract_first()
            if product_url:
                absolute_url = urljoin("https://www.flipkart.com/", product_url)
                yield scrapy.Request(url=absolute_url, callback=self.parse_product_data, meta={'page':page}, headers=self.headers)

        # You can continue to the next page if needed
        next_page = response.css('a._1LKTO3::attr(href)').extract_first()
        if next_page:
            next_page_url = urljoin(response.url, next_page)
            yield scrapy.Request(url=next_page_url, callback=self.discover_product_urls, meta={'page': page + 1}, headers=self.headers)

    def parse_product_data(self, response):
        #image_data = json.loads(re.findall(r"colorImages':.*'initial':\s*(\[.+?\])},\n", response.text)[0])
        script_text = response.xpath('//script[contains(., "colorImages")]/text()').get()
        image_data = json.loads(re.search(r'colorImages":(.+?),"max_order', script_text).group(1))
        #variant_data = re.findall(r'dimensionValuesDisplayData"\s*:\s* ({.+?}),\n', response.text)
        #feature_bullets = [bullet.strip() for bullet in response.css("#feature-bullets li ::text").getall()]
        seller_name = response.css('div#sellerName span span ::text').get("")
        seller_rating = response.css('div._1D-8OL ::text').get("")
        star = response.css("div._2d4LTz ::text").get()
        if not star:
            star = "NA"
        price = response.css('._16Jk6d[aria-hidden="true"] ::text').get("")
        if not price:
            price = response.css('._16Jk6d::text').get("")
        yield {
            "name": response.css("span.B_NuCI::text").get("").strip(),
            "price": price,
            "sellerName":seller_name,
            "SellerRating":seller_rating,
            "stars": star,
            "images": image_data,
        }