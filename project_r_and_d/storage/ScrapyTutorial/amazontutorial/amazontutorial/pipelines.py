# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import mysql.connector

class AmazontutorialPipeline:
    # initiate
    def __init__(self):
        self.create_connection()
        self.create_table()
    # create connection

    def create_connection(self):
        self.conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            passwd = 'aingg',
            database = 'amazon_test'
        )
        self.curr = self.conn.cursor()
    # create table
    
    def create_table(self):
        self.curr.execute("""DROP TABLE IF EXISTS amazon_tb""")
        self.curr.execute("""create table amazon_tb(
            product_name text,
            product_author text,
            product_price text,
            product_imagelink text
        )""")

    # store db
    def store_db(self, item):
        self.curr.execute("""insert into amazon_tb values (%s,%s,%s,%s)""", (
            item['product_name'][0],
            item['product_author'][0],
            item['product_price'][0],
            item['product_imagelink'][0]
        ))
        self.conn.commit()
    
    # process item to store in database
    def process_item(self, item, spider):
        self.store_db(item)
        return item
