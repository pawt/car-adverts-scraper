from scrapy import signals
from scrapy.mail import MailSender
from sqlalchemy.orm import sessionmaker
from models import CarAdverts, db_connect
import sendgrid
import os
from sendgrid.helpers.mail import *

NEW_ADVERTS_HEADER = "\n\n ######## NOWE OGLOSZENIA ########\n\n"

def set_db_session():
    '''

    :return:
    '''
    #establishing connection to DB
    engine = db_connect("heroku")
    #engine = db_connect("local")
    session = sessionmaker(bind=engine)
    return session()

def set_mailsent_to_true(session, sqlObjects):
    '''

    :param session:
    :param sqlObjects:
    :return:
    '''
    for advert in sqlObjects:
        print("Updating mailsent value to TRUE for advert (id = %s, title = %s)" % (advert.id, advert.title))
        session.query(CarAdverts).filter(CarAdverts.id == advert.id).update({'mailsent': True})
        session.commit()

def get_new_items_from_DB(session):
    '''

    :param session:
    :return:
    '''
    try:
        new_adverts = session.query(CarAdverts).filter(CarAdverts.mailsent == False).all()
        set_mailsent_to_true(session, new_adverts)
    except Exception as e:
        print(">> Exception caught: %s" % e)
        new_adverts = ''
    finally:
        session.close()

    return new_adverts

def remove_nonexistent_items_from_DB(session):
    '''

    :param session:
    :return:
    '''
    invalid_adverts = session.query(CarAdverts).filter(CarAdverts.isvalid == False).all()
    if invalid_adverts:
        for advert in invalid_adverts:
            print("INFO: Removing nonexistent advert from database (id = %s; title = %s)" % (advert.id, advert.title))
            session.delete(advert)
            session.commit()
    else:
        print("INFO: No nonexistent adverts found in DB.")

def update_isvalid_column_in_DB(session):
    '''

    :param session:
    :return:
    '''
    print("INFO: Updating isvalid column in DB...")
    all_adverts = session.query(CarAdverts).all()
    for advert in all_adverts:
        session.query(CarAdverts).filter(CarAdverts.id == advert.id).update({'isvalid': False})
        session.commit()

def parse_new_adverts(newAdvertsObjects):
    '''

    :param newAdvertsObjects:
    :return:
    '''
    final_list = []
    for new_advert in newAdvertsObjects:
        final_list.append("\n".join(new_advert.getInfo()))
        final_list.append("-" * 100)
    return '\n'.join(final_list)


class StatusMailer(object):
    '''
    tbd
    '''
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

        getSession = set_db_session()
        getSession.expire_on_commit = False

        spider_stats = self.stats.get_stats(spider)

        try:
            new_adverts = parse_new_adverts(get_new_items_from_DB(getSession))
            remove_nonexistent_items_from_DB(getSession)
            update_isvalid_column_in_DB(getSession)
        except:
            getSession.rollback()
            raise
        finally:
            print("INFO: closing the connection to DB...")
            getSession.close()

        #formatting dictionary as a string (body msg of the email)
        spiderstats_string = '\n'.join('{} : {}'.format(key, val) for key, val in sorted(spider_stats.items()))

        if new_adverts:
            print("INFO: New adverts found! trying to send e-mail...")
            print("INFO: self.recipients: " + str(self.recipients))
            sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
            from_email = Email(os.environ.get('SENDGRID_USERNAME'))
            subject = "Nowe ogloszenia - otomoto.pl"
            to_email = Email(self.recipients)
            body = NEW_ADVERTS_HEADER + new_adverts.encode('utf-8') + "<br> ================================== <br>" + spiderstats_string
            content = Content("text/html", body)
            mail = Mail(from_email, subject, to_email, content)
            response = sg.client.mail.send.post(request_body=mail.get())
            print("Response status code: " + str(response.status_code))
        else:
            print("INFO: No new adverts scraped -> email is not sent.")

        # if new_adverts:
        #     print("INFO: New adverts found! trying to send e-mail...")
        #     print("INFO: self.recipients: " + str(self.recipients))
        #     self.mail.send(
        #         to=self.recipients,
        #         subject='Crawler for %s' % (spider.name),
        #         body=NEW_ADVERTS_HEADER +
        #              new_adverts.encode('utf-8') +
        #              "\n =================================== \n" +
        #              spiderstats_string
        #     )
        # else:
        #     print("INFO: No new adverts scraped -> email is not sent.")

