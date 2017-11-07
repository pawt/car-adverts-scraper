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
        "https://www.otomoto.pl/osobowe/lodz/-/-/-/-/minivan--sedan--suv/?search%5Bfilter_float_price%3Afrom%5D=15000&search%5Bfilter_float_price%3Ato%5D=30000&search%5Bfilter_enum_has_vin%5D=1&search%5Bfilter_float_year%3Afrom%5D=2005&search%5Bfilter_float_year%3Ato%5D=2016&search%5Bfilter_enum_fuel_type%5D%5B0%5D=diesel&search%5Bfilter_enum_fuel_type%5D%5B1%5D=petrol-lpg&search%5Bfilter_enum_damaged%5D=0&search%5Bfilter_float_nr_seats%3Afrom%5D=5&search%5Bfilter_enum_rhd%5D=0&search%5Bfilter_enum_features%5D%5B0%5D=abs&search%5Bfilter_enum_features%5D%5B1%5D=central-lock&search%5Bfilter_enum_no_accident%5D=1&search%5Bbrand_program_id%5D%5B0%5D=&search%5Bdist%5D=100&search%5Bcountry%5D=polska"
    ]

    def parse(self, response):
        for sel in response.xpath('//section[@id="om-list-items"]//article[@id]'):
            item = CarAdvertsItem()
            item['title'] = sel.xpath('h2/a[@class="offer-title__link"]/text()').extract()[0].strip()
            item['price'] = sel.xpath('div[@class="offer-price"]/span[@class="offer-price__number"]/text()').extract()[0].strip()
            item['year'] = sel.xpath('li[@class="offer-item__params-item"[0]]/span/text()').extract()[0]
            item['location'] = sel.xpath('aside/strong/text()').extract()[0].strip()
            item['link'] = "http://www.otomoto.pl" + str(sel.xpath('aside/a/@href').extract()[0])
            item['date'] = strftime("%Y-%m-%d %H:%M:%S")
            #print(location.encode('utf-8'))
            yield item
