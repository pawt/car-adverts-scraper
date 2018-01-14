__author__ = 'pawt'

import scrapy
from carAdverts.items import CarAdvertsItem
from time import strftime

class OtoMotoSpider(scrapy.Spider):
    name = "otomoto"
    allowed_domains = ["otomoto.pl"]
   # start_urls = [
   #     "http://otomoto.pl/osobowe?s=dd&l=60&fq%5Blocation_type%5D=post_code_range&fq%5Bpost_code%5D%5Brange%5D=75&fq%5Bpost_code%5D%5Bpostcode%5D=94-102&fq%5Bprice%5D%5Bfrom%5D=10000&fq%5Bprice%5D%5Bto%5D=17000&fq%5Bcomfort%5D%5B0%5D=item.has_air_conditioning&fq%5Bdoors_number%5D%5B0%5D=4%2F5&fq%5Borigin_country%5D=PL&fq%5Bregistration_country%5D=PL&fq%5Btechnical_condition%5D=functioning&fq%5Bhistory%5D%5B0%5D=item.has_no_accident&fq%5Bhistory%5D%5B1%5D=item.has_authorized_service&fq%5Badvertiser_type%5D%5B0%5D=individual&fq%5Badvert_features%5D%5B0%5D=has_photos",
   #     "http://otomoto.pl/osobowe?s=dd&l=60&q=Toyota+Corolla+Seria+E12&fq%5Blocation_type%5D=post_code_range&fq%5Bpost_code%5D%5Brange%5D=75&fq%5Bpost_code%5D%5Bpostcode%5D=94-102&fq%5Bcomfort%5D%5B0%5D=item.has_air_conditioning&fq%5Bdoors_number%5D%5B0%5D=4%2F5&fq%5Borigin_country%5D=PL&fq%5Bregistration_country%5D=PL&fq%5Btechnical_condition%5D=functioning&fq%5Bhistory%5D%5B0%5D=item.has_no_accident&fq%5Badvertiser_type%5D%5B0%5D=individual&fq%5Badvert_features%5D%5B0%5D=has_photos"
   # ]

    start_urls = [
        "https://www.otomoto.pl/osobowe/grotniki/citroen/c5/iii-2008/?search[filter_enum_fuel_type][0]=diesel&search[filter_enum_damaged]=0&search[filter_enum_rhd]=0&search[brand_program_id][0]=&search[dist]=25&search[country]="
    ]

    def parse(self, response): 
        #for sel in response.xpath('//div[@id="listContainer"]//article[@class="offer.item"]'):
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
