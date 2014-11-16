from scrapy import signals
from scrapy.mail import MailSender
from sqlalchemy.orm import sessionmaker
from models import CarAdverts, db_connect

def setDBsession():
    #establishing connection to DB
    engine = db_connect()
    session = sessionmaker(bind=engine)
    return session()

def set_mailsent_to_true(session, sqlObjects):
    for entry in sqlObjects:
        print("Updating object (id=%s) in DB" % entry.id)
        session.query(CarAdverts).filter(CarAdverts.id == entry.id).update({'mailsent': True})
        session.commit()

def get_new_items_from_DB():
    getSession = setDBsession()

    try:
        new_adverts = getSession.query(CarAdverts).filter(CarAdverts.mailsent == False).all()
        set_mailsent_to_true(getSession, new_adverts)
    except Exception as e:
        print(">> Exception caught: %s" % e)
        new_adverts = ''
    return new_adverts

def parse_new_adverts(newAdvertsObjects):
    final_list = ["\n\n ######## NEW ADVERTS: ########\n\n"]
    for new_advert in newAdvertsObjects:
        final_list.append("\n".join(new_advert.getInfo()))
        final_list.append("-----------------------------")
    return '\n'.join(final_list)


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

        new_adverts = parse_new_adverts(get_new_items_from_DB())

        #formatting dictionary as a string (body msg of the email)
        spiderstats_string = '\n'.join('{} : {}'.format(key, val) for key, val in sorted(spider_stats.items()))

        if new_adverts:
            self.mail.send(
                to=self.recipients,
                subject='Crawler for %s' % (spider.name),
                body= spiderstats_string + new_adverts.encode('utf-8')
            )
        else:
            print("INFO: No new adverts scraped -> email is not sent.")