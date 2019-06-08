# -*- coding: utf-8 -*-
import scrapy


class GirlSpider(scrapy.Spider):
    name = 'girl'
    allowed_domains = ['girl13.com']
    start_urls = ['http://www.girl13.com/']


    def parse(self, response):
        divs = response.xpath('//div[@class="column-post"]')
        for div in divs:
            img_url = div.xpath('.//img/@src').get()
            tag  = '-'.join(div.xpath('./p[@class="entry-tags"]/a/text()').getall())

            item = {'tag':tag,'img_url':img_url}
            yield item


        next_url = response.xpath('//li[@class="next"]/a/@href').get()
        if next_url:
            yield scrapy.Request(url=next_url,
                                 callback=self.parse)