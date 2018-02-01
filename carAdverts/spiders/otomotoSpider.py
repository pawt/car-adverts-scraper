__author__ = 'pawt'

import scrapy
from carAdverts.items import CarAdvertsItem
from time import strftime

class OtoMotoSpider(scrapy.Spider):
    name = "otomoto"
    allowed_domains = ["otomoto.pl"]

    start_urls = [
        "https://www.otomoto.pl/osobowe/grotniki/citroen/c5/iii-2008/?search[filter_enum_fuel_type][0]=diesel&search[filter_enum_damaged]=0&search[filter_enum_rhd]=0&search[brand_program_id][0]=&search[dist]=25&search[country]=",
        "https://www.otomoto.pl/osobowe/grotniki/fiat/freemont/?search%5Bbrand_program_id%5D%5B0%5D=&search%5Bdist%5D=25&search%5Bcountry%5D="
    ]

    def parse(self, response): 
        links = response.xpath('//div[@id="listContainer"]//div[@class="offer-item__content"]')
        for sel in links:
            #print(sel.extract())
            item = CarAdvertsItem()
            item['title'] = sel.xpath('div[@class="offer-item__title"]/h2[@class="offer-title"]/a[@class="offer-title__link"]/text()').extract()[0].strip()
            item['price'] = sel.xpath('div[@class="offer-item__price"]/div[@class="offer-price"]/span[@class="offer-price__number"]/text()').extract()[0].strip()
            item['year'] = sel.xpath('ul[@class="offer-item__params"]/li[contains(@data-code, "year")]/span/text()').extract()[0]
            item['location'] = sel.xpath('div[@class="offer-item__bottom-row "]/span[@class="offer-item__location"]/h4/text()').extract()[0].strip()
            item['link'] = sel.xpath('div[@class="offer-item__title"]/h2[@class="offer-title"]/a[@class="offer-title__link"]/@href').extract()[0]
            item['date'] = strftime("%Y-%m-%d %H:%M:%S")
            #print(location.encode('utf-8'))
            yield item
