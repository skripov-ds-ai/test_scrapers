# -*- coding: utf-8 -*-
import scrapy
from scrapy import signals

import random
import time

from ajax_pagination.items import AjaxPaginationItem

from scrapy.selector import Selector

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class EcommerceAjaxPaginationSpider(scrapy.Spider):
    name = 'ecommerce_ajax_pagination_spider'
    start_urls = [
        "https://www.webscraper.io/test-sites/e-commerce/ajax/product/251",
    ]

    def __init__(self):
        super().__init__()
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--no-sandbox')
        self.options.add_argument("--headless")

    def parse(self, response):
        if 'ajax' in response.url:

            big_hrefs = []

            if 'product' in response.url:
                sel = Selector(response)

                item = AjaxPaginationItem()
                item['name'] = sel.xpath(
                    r"//div[@class='caption']/h4[position()=2]/text()"
                ).extract_first().strip()
                item['price'] = sel.xpath(
                    r"//*[contains(@class, 'price')]/text()"
                ).extract_first().strip()
                item['description'] = sel.xpath(
                    r"//*[contains(@class, 'description')]/text()"
                ).extract_first().strip()
                item['reviews_count'] = sel.xpath(
                    r"//*[contains(@class, 'ratings')]/p/text()"
                ).extract_first().strip()
                item['rating'] = (len(sel.xpath(
                    r"//*[contains(@class, 'ratings')]/p/span"
                ).extract()))

                yield item
            else:
                driver = webdriver.Chrome(
                    '/home/nizhikebinesi/scrapers_for_test_sites/ajax_pagination/ajax_pagination/spiders/chromedriver',
                    chrome_options=self.options
                )
                driver.set_window_size(1024, 768)

                driver.get(response.url)
                driver.implicitly_wait(2 * random.random() / 3)

                buttons = driver.find_elements_by_class_name('pagination')
                if len(buttons) > 0:
                    buttons = buttons[0].find_elements_by_tag_name('button')

                body = driver.find_element_by_tag_name('body')

                for i, button in enumerate(buttons):
                    for j in range(int(10 * random.random() / 7)):
                        driver.implicitly_wait(0.21 + 5 * random.random() / 7)
                        body.send_keys(Keys.PAGE_DOWN)

                    time.sleep(2.13 + random.random())
                    driver.implicitly_wait(2.3 + random.random() * 1.5)
                    if i > 1:
                        button.click()
                        driver.implicitly_wait(1.09 + random.random() * 1.5)
                    time.sleep(4.72)

                    for j in range(int(2.2 * random.random())):
                        driver.implicitly_wait(1.21 + random.random())
                        body.send_keys(Keys.PAGE_UP)
                    time.sleep(3.220222 + random.random() / 10)

                    hrefs = list(
                        map(
                            lambda x: x.get_attribute('href').strip(),
                            driver.find_elements_by_xpath('//a[@class="title"]')
                        )
                    )
                    big_hrefs.extend(hrefs)
                driver.quit()

            hrefs = list(filter(lambda x: 'ajax' in x, response.xpath('//a/@href').getall()))
            hrefs.extend(big_hrefs)

            for href in hrefs:
                yield scrapy.Request(response.urljoin(href), self.parse)




