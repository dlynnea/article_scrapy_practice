# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class ArticlesSpider(scrapy.Spider):
    name = 'articles'
    allowed_domains = ['www.bbc.com']
    start_urls = ['https://www.bbc.com/travel/columns/culture-identity']


    # rules = (
    #     Rule(LinkExtractor(restrict_xpaths=("//div[@class='load-more-button']/a")))
    #     Rule(LinkExtractor(restrict_xpaths=("//div[@class='load-more-button']/a")))
    # )

    # user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'

    # def start_request(self):
    #     yield scrapy.Request(url='https://www.bbc.com/travel', headers={
    #         'User-Agent': self.user_agent
    #     })

    def parse(self, response):
        for article in response.xpath("//ul[@class='article-list article-list-group-1 ']/li"):
            yield {
                'title': article.xpath(".//h3[@class='promo-unit-title']/text()").get(),
                'url': response.urljoin(article.xpath(".//div[@class='promo-unit-header promo-unit-header-with-context']/a/@href").get()),
                'p': article.xpath(".//p[@class='promo-unit-summary']/text()").get()
            }
        
        next_page = response.xpath("//div[@class='load-more-button']/a/@href").get()

        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse)
