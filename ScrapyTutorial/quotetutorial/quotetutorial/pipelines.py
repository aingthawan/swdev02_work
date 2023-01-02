# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3

class QuotetutorialPipeline:

    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):
        # create connection
        self.conn = sqlite3.connect('myQuotes.db')
        # crate cursor
        self.curr = self.conn.cursor()

    def create_table(self):
        # crate table if not exist
        self.curr.execute("""DROP TABLE IF EXISTS quotes_tb""")
        self.curr.execute("""create table quotes_tb(
            title text,
            author text,
            tags text
        )""")
    
    # function to store data to database
    def store_db(self, item):
        self.curr.execute("""insert into quotes_tb values (?,?,?)"""(
            item['title'][0],
            item['author'][0],
            item['tags'][0]
        ))
        self.conn.commit()

    # program jumps here after init
    def process_item(self, item, spider):
        self.store_db(item)
        # print("Pipeline :" + item['title'][0])
        return item
