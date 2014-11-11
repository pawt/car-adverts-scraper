from scrapy import signals
from scrapy.mail import MailSender
from sqlalchemy.orm import sessionmaker
from models import CarAdverts, db_connect

def get_new_items_from_DB():
    #establishing connection to DB
    engine = db_connect()
    session = sessionmaker(bind=engine)
    getSession = session()
    tmp_advert = getSession.query(CarAdverts).filter(CarAdverts.year == "2007").one()
    return tmp_advert.title


class StatusMailer(object):

    def __init__(self, stats, mail, recipients):
        self.stats = stats
        self.mail = mail
        self.recipients = recipients

    @classmethod
    def from_crawler(cls, crawler):

        recipients = crawler.settings.getlist('STATUSMAILER_RECIPIENTS')
        mail = MailSender.from_settings(crawler.settings)

        ext = cls(crawler.stats, mail, recipients)

        crawler.signals.connect(ext.spider_closed, signal=signals.spider_closed)

        return ext

    def spider_closed(self, spider):
        spider_stats = self.stats.get_stats(spider)
        new_items = get_new_items_from_DB()
        #formatting dictionary as a string (body msg of the email)
        spiderstats_string = '\n'.join('{} : {}'.format(key, val) for key, val in sorted(spider_stats.items()))

        self.mail.send(
            to=self.recipients,
            subject='Crawler for %s' % (spider.name),
            body= spiderstats_string + "\n\n" + new_items.encode('utf-8')
        )