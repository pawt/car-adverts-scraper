# -*- coding: utf-8 -*-

# Scrapy settings for carAdverts project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#
import os

BOT_NAME = 'carAdverts'

SPIDER_MODULES = ['carAdverts.spiders']
NEWSPIDER_MODULE = 'carAdverts.spiders'

DATABASE = {'drivername': '',
            'host': '',
            'port': '',
            'username': '',
            'password': '',
            'database': ''}     


ITEM_PIPELINES = {'carAdverts.pipelines.CarAdvertsPipeline': 1}

EXTENSIONS = {'carAdverts.extensions.StatusMailer': 500}

try:
    MAIL_HOST = os.environ['MAIL_HOST']
    MAIL_PORT = os.environ['MAIL_PORT']
    MAIL_USER = os.environ['MAIL_USER']
    MAIL_PASS = os.environ['MAIL_PASS']
    STATUSMAILER_RECIPIENTS = [os.environ['STATUSMAILER_RECIPIENTS']]
except KeyError:
    pass

try:
    from settings_dev import *
except ImportError:
    pass

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'carAdverts (+http://www.yourdomain.com)'
