# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

class ArchiveSpider(scrapy.Spider):
    name = 'archive'
    allowed_domains = ['www.quantamagazine.org']
    start_urls = ['https://www.quantamagazine.org/abstractions']

    # rules = (
    #     Rule(LinkExtractor(restrict_xpaths=("//a[@class='inline-block pv05']/@href"), callback=parse, follow=True))
    # )

    def parse(self, response):
        articles = response.xpath("//div[@class='card clearfix mv05 pv1']")
        for article in articles:
            yield {
                'title': article.xpath(".//h2[@class='card__title noe mv0 theme__accent-hover transition--color']/text()").get(),
                'author': article.xpath(".//h6[@class='byline relative flex flex-items-start merriweather mv025 mr1 gray3 theme__text-hover']/a/span/text()").get(),
                'url': response.urljoin(article.xpath(".//div[@class='card__image mr1 mb1']/a/@href").get()),
                'summary': article.xpath(".//div[@class='card__excerpt h5 mt025 pangram o6']/p/text()").get()
            }

        next_page = response.urljoin(response.xpath("//a[@class='inline-block pv05']/@href").get())

        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse)
