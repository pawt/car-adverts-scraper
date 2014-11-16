__author__ = 'pawt'

import scrapy
from carAdverts.items import CarAdvertsItem
from time import strftime

class OtoMotoSpider(scrapy.Spider):
    name = "otomoto"
    allowed_domains = ["otomoto.pl"]
    #start_urls = [
    #    "http://otomoto.pl/osobowe/////hatchback,pickup,sportowy-coupe?s=dd&l=60&fq%5Blocation_type%5D=post_code_range&fq%5Bpost_code%5D%5Brange%5D=75&fq%5Bpost_code%5D%5Bpostcode%5D=94-102&fq%5Bprice%5D%5Bfrom%5D=10000&fq%5Bprice%5D%5Bto%5D=17000&fq%5Bcomfort%5D%5B0%5D=item.has_air_conditioning&fq%5Bdoors_number%5D%5B0%5D=4%2F5&fq%5Borigin_country%5D=PL&fq%5Btechnical_condition%5D=functioning&fq%5Bhistory%5D%5B0%5D=item.has_no_accident&fq%5Bhistory%5D%5B1%5D=item.has_first_owner&fq%5Bhistory%5D%5B2%5D=item.has_authorized_service&fq%5Badvertiser_type%5D%5B0%5D=individual&fq%5Badvert_features%5D%5B0%5D=has_photos"
    #]
    start_urls = [
        "http://otomoto.pl/osobowe/////hatchback,pickup,sportowy-coupe?s=dd&l=60&fq%5Blocation_type%5D=post_code_range&fq%5Bpost_code%5D%5Brange%5D=75&fq%5Bpost_code%5D%5Bpostcode%5D=94-102&fq%5Bprice%5D%5Bfrom%5D=10000&fq%5Bprice%5D%5Bto%5D=17000&fq%5Bcomfort%5D%5B0%5D=item.has_air_conditioning&fq%5Bdoors_number%5D%5B0%5D=4%2F5&fq%5Borigin_country%5D=PL&fq%5Btechnical_condition%5D=functioning&fq%5Bhistory%5D%5B0%5D=item.has_no_accident&fq%5Bhistory%5D%5B1%5D=item.has_authorized_service&fq%5Badvertiser_type%5D%5B0%5D=individual&fq%5Badvert_features%5D%5B0%5D=has_photos"
    ]

    def parse(self, response):
        for sel in response.xpath('//section[@id="om-list-items"]//article[@id]'):
            item = CarAdvertsItem()
            item['title'] = sel.xpath('h3/a/text()').extract()[0].strip()
            item['price'] = sel.xpath('p/span/strong[@class="om-price-amount"]/text()').extract()[0].strip()
            item['year'] = sel.xpath('p[@class="basic"]/span/strong/text()').extract()[0]
            item['location'] = sel.xpath('aside/strong/text()').extract()[0].strip()
            item['link'] = "http://www.otomoto.pl" + str(sel.xpath('aside/a/@href').extract()[0])
            item['date'] = strftime("%Y-%m-%d %H:%M:%S")
            #print(location.encode('utf-8'))
            yield item
