import json
import scrapy
from urllib.parse import urljoin
import re
from datetime import datetime
from amazon_scraping.items import AmazonProduct

class AmazonSearchProductSpider(scrapy.Spider):
    name = "amazon_search_product"

    custom_settings = {
    'FEEDS': {
        'data/%(name)s_%(time)s.json': {
            'format': 'json',
            # Use strftime to format the current time with hour and minute
            'time': datetime.now().strftime('%Y-%m-%d_%H-%M'),
        }
         }
        }

    def start_requests(self):
        keyword_list = ['ipad']
        for keyword in keyword_list:
            amazon_search_url = f'https://www.amazon.com/s?k={keyword}&page=1'
            yield scrapy.Request(url=amazon_search_url, callback=self.discover_product_urls, meta={'keyword': keyword, 'page': 1})

    def discover_product_urls(self, response):
        page = response.meta['page']
        keyword = response.meta['keyword'] 

        ## Discover Product URLs
        search_products = response.css("div.s-result-item[data-component-type=s-search-result]")
        for product in search_products:
            relative_url = product.css('h2 a.a-link-normal').attrib['href']
            product_url = urljoin('https://www.amazon.com/', relative_url)
            yield scrapy.Request(url=product_url, callback=self.parse_product_data, meta={'keyword': keyword, 'page': page})
            
        ## Get All Pages
        if page == 1:
            available_pages = response.xpath(
                '//*[contains(@class, "s-pagination-item")][not(has-class("s-pagination-separator"))][not(has-class("s-pagination-previous"))]/text()'
            ).getall()

            last_page = available_pages[-1]
            for page_num in range(2, int(last_page)+1):
                amazon_search_url = f'https://www.amazon.com/s?k={keyword}&page={page_num}'
                yield scrapy.Request(url=amazon_search_url, callback=self.discover_product_urls, meta={'keyword': keyword, 'page': page_num})


    def parse_product_data(self, response):
        feature_bullets = [bullet.strip() for bullet in response.css("#feature-bullets li ::text").getall()] # strip to remove extra whitespaces
        price = response.css('span.a-price-whole ::text').get()
        amazon_product = AmazonProduct()
        
        amazon_product["name"] = response.css("#productTitle::text").get("").strip() # type: ignore
        amazon_product["relative_url"] = response.url # type: ignore
        amazon_product["price"] = price
        amazon_product["stars"] = response.css('i.a-icon ::text').get("").strip()
        amazon_product["rating_count"] = response.css('#acrCustomerReviewText ::text').get("").strip()
        amazon_product["feature_bullets"] = feature_bullets

        yield amazon_product
        