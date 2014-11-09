# -*- coding: utf-8 -*-

# Scrapy settings for carAdverts project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'carAdverts'

SPIDER_MODULES = ['carAdverts.spiders']
NEWSPIDER_MODULE = 'carAdverts.spiders'

DATABASE = {'drivername': 'postgres',
            'host': 'localhost',
            'port': '5432',
            'username': 'postgres',
            'password': 'red-devils',
            'database': 'scrapydb'}

ITEM_PIPELINES = {'carAdverts.pipelines.CarAdvertsPipeline' : 1 }


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'carAdverts (+http://www.yourdomain.com)'
