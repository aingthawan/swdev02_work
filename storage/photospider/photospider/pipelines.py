# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import mysql.connector

class PhotospiderPipeline:

    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            passwd = 'aingg',
            database = '35mmc'
        )
        self.curr = self.conn.cursor()

    def create_table(self):
        self.curr.execute("""DROP TABLE IF EXISTS 35mmc_raw""")
        self.curr.execute("""create table 35mmc_raw(
            title text,
            url text,
            related_url text,
            raw_html text
        )""")
    
    def store_db(self, item):
        self.curr.execute("""insert into 35mmc_raw values (%s, %s, %s, %s)""", (
            item['title'],
            item['url'],
            item['related_url'],
            item['raw_html']
        ))
        self.conn.commit()

    def process_item(self, item, spider):
        self.store_db(item)
        return item
