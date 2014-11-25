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

DATABASE = {'drivername': '',
            'host': '',
            'port': '',
            'username': '',
            'password': '',
            'database': ''}

DATABASE_HEROKU = {'drivername': 'postgres',
                'host': 'ec2-54-204-45-126.compute-1.amazonaws.com',
                'port': '5432',
                'username': 'hiuiuotcxvgjdi',
                'password': 'iygllY6zpSU-65tDxoTqyRRKcp',
                'database': 'ddm9pfqo83f4oc'}


ITEM_PIPELINES = {'carAdverts.pipelines.CarAdvertsPipeline': 1}

EXTENSIONS = {'carAdverts.extensions.StatusMailer': 500}

#STATUSMAILER_RECIPIENTS = [""]
MAIL_HOST = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USER = 'pawt87'
MAIL_PASS = 'DexterMorgan16'
STATUSMAILER_RECIPIENTS = ["ptrybulski@gmail.com"]

try:
    from settings_dev import *
except ImportError:
    pass

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'carAdverts (+http://www.yourdomain.com)'
