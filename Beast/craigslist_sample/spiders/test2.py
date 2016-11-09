import scrapy
import re
import os.path
from lxml import etree
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from craigslist_sample.items import BeastItem
from scrapy.utils.response import body_or_str

class MySpider(CrawlSpider):
    name = "beast"
    allowed_domains = ["thedailybeast.com"]
    start_urls = ["http://www.thedailybeast.com/"]

    base_url = 'http://www.thedailybeast.com/sitemap/'
    year = ['2016','2015','2014','2013','2012','2011','2010','2009','2008']
    month = ['12','11','10','09','08','07','06','05','04','03','02','01']

    def parse(self,response):
        for y in self.year:
            for m in self.month:
#                 for d in self.day:
                    url = self.base_url+y+'/'+m+'/articles.html'
                    yield scrapy.Request(url,self.parseList)

    def parseList(self, response):
        sel = Selector(response)
        articles = sel.xpath('//div[@class="first-column"]/ul/li/a').extract()
        for article in articles:
            root = etree.fromstring(article)
            link = root.attrib['href']
            yield scrapy.Request(link,self.parse_items)

    def parse_items(self, response):
        hxs = Selector(response)
        items = []
        item = BeastItem()
        item["title"] = hxs.xpath('//h1[@class="Title"]/text()').extract()[0]
        article = hxs.xpath('//div[@class="Text"]/p/text()').extract()
        item["article"] = "\n".join(article).encode('utf8')
        item['link'] = response.url
#        item["date"] = hxs.xpath('//h4[@class="date-time"]/text()').extract()[0].encode('utf8')
        items.append(item)

        return items