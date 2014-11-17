# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from sqlalchemy.orm import sessionmaker
from models import CarAdverts, db_connect, create_adverts_table


class CarAdvertsPipeline(object):
    """CarAdverts pipeline for storing scraped items in the database"""
    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        Creates deals table.
        """
        engine = db_connect()
        create_adverts_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        """Save car deals in the database.

        This method is called for every item pipeline component.

        """
        session = self.Session()
        advert = CarAdverts(**item)

        try:
            #checking if the particular advert is already in database
            if not session.query(CarAdverts).filter(CarAdverts.link==advert.link).count():
                session.add(advert)
                session.commit()
            else:
                print("INFO: advert (title = %s) still exists." % advert.title)
                session.query(CarAdverts).filter(CarAdverts.link == advert.link).update({'isvalid': True})
                session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return item