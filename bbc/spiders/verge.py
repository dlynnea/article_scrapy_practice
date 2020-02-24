# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class VergeSpider(scrapy.Spider):
    name = 'verge'
    allowed_domains = ['www.theverge.com']
    start_urls = ['https://www.theverge.com/energy']

    def parse(self, response):
        articles = response.xpath("//div[@class='c-entry-box--compact c-entry-box--compact--article']")
        for article in articles:
            yield {
                'title': article.xpath(".//h2[@class='c-entry-box--compact__title']/a/text()").get(),
                'url': article.xpath(".//a/@href").get(),
                'author': article.xpath(".//span[@class='c-byline__author-name']/text()").get()
            }
