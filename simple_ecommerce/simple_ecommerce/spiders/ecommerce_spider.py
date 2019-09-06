# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from simple_ecommerce.items import Product

import time
import random


class EcommerceSpiderSpider(CrawlSpider):
    name = 'ecommerce_spider'
    allowed_domains = [
        'scrapingclub.com'
    ]
    start_urls = [
        'https://scrapingclub.com/exercise/list_basic/'
    ]
    rules = (
        Rule(
            LinkExtractor(
                allow=(
                    'scrapingclub.com/exercise/list_basic/\?*'
                ),
                unique=True,
            ),
        ),
        Rule(
            LinkExtractor(
                allow=(
                    'scrapingclub.com/exercise/list_basic_detail/*'
                ),
                unique=True,
            ),
            callback='parse_item'
        ),
    )

    def parse_item(self, response):
        time.sleep(random.random() + 0.1)
        if round(random.random() * 10) / 7 > 3.1:
            time.sleep(0.3 + 1.073 * random.random() / 13)

        item = Product()
        item['title'] = response.css(
            'h3.card-title::text'
        ).get().strip()

        img_src = response.css(
            'img.card-img-top::attr(src)'
        ).get()
        item['image'] = response.urljoin(img_src)

        price = response.xpath(
            '//div[@class="card-body"]/h4/text()'
        ).get().strip()
        price_num = price[1:]
        price_currency = price[0]

        item['price'] = price_num
        item['currency'] = price_currency
        item['description'] = response.css(
            'p.card-text::text'
        ).get().strip()

        yield item

