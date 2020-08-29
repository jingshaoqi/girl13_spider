# -*- coding: utf-8 -*-
import scrapy


class GirlSpider(scrapy.Spider):
    name = 'girl'
    allowed_domains = ['girl13.com']
    start_urls = ['http://www.girl13.com/']
    print('start urls:{00000000000000000000000000000}')

    def parse(self, response):
        print('response----------------------------a----------------')
        divs = response.xpath('//div[@class="column-post"]')
        for div in divs:
            img_url = div.xpath('.//img/@src').get()
            tag = '-'.join(div.xpath('./p[@class="entry-tags"]/a/text()').getall())

            item = {'tag':tag,'img_url':img_url}
            print('tag:{} img_url:{}'.format(tag,img_url))
            yield item
        next_url = response.xpath('//li[@class="next"]/a/@href').get()
        print('next_url:{}'.format(next_url))
        if next_url:
            yield scrapy.Request(url=next_url, callback=self.parse)