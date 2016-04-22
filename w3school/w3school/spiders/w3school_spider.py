#!/usr/bin/python
# -*- coding: utf-8 -*-


from scrapy.spiders import Spider
from scrapy.selector import Selector
#from scrapy import log


from w3school.items import W3schoolItem


class W3schoolSpider(Spider):
    """爬取w3school标签"""
    name = "w3school"
    allowed_domains = ["w3school.com.cn"]
    start_urls = [
        "http://www.w3school.com.cn/xml/index.asp"
        ]

    def parse(self, response):
        sel = Selector(response)
        sites = sel.xpath('//div[@id="navsecond"]/div[@id="course"]/ul/li')
        items = []

        for site in sites:
            item = W3schoolItem()

            title = site.xpath('a/text()').extract()
            link = site.xpath('a/@href').extract()
            desc = site.xpath('a/@title').extract()

            item['title'] = [t.encode('utf-8') for t in title]
            item['link'] = [l.encode('utf-8') for l in link]
            item['desc'] = [d.encode('utf-8') for d in desc]

            items.append(item)

 #           log.logger("Appending item ...", level='INFO')

#      log.logger("Append done", level='INFO')
        return  items





