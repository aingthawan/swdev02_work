# A code to scrape name from 35mmc.com
# scrape for a defined level
# Aing KK.

from tqdm import tqdm
import concurrent.futures
import requests
from bs4 import BeautifulSoup
import mysql.connector

def crawl_level(db, url, level):
    # depth limit for crawling url
    if level <= 20:
        # print("Crawling level : ", level)
        webReq = requests.get(url)
        soup_obj = BeautifulSoup(webReq.text, "html.parser")
        raw_text = soup_obj.find('article').text
        # get title
        get_title = soup_obj.find('h1', {'class':'entry-title'}).text
        print(get_title)
        # store to db
        db.store_db(get_title, url, raw_text)
        return [i.find('a')['href'] for i in soup_obj.find_all('div', {'class':'sp-col-4'})]
    else:
        return []

def crawl_3level(db, url, level):
    links = crawl_level(db, url, level)
    # parallel scraping
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_url = {executor.submit(crawl_3level, db, link, level+1): link for link in links}
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                future.result()
            except Exception as exc:
                print('%r generated an exception: %s' % (url, exc))

class databasePipeline:
    def __init__(self, host, user, password, database, table_name):
        print("Initialize Database Pipeline")
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.table_name = table_name
        self.create_connection()
        self.curr = self.conn.cursor()
        self.create_table()

    def create_connection(self):
        """Create a connection to the database"""
        print("Creating Connection . . .")
        self.conn = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        print("Connceted.")
    
    def create_table(self):
        print("Creating table . . .")
        self.curr.execute("""DROP TABLE IF EXISTS 35mmc_raw""")
        self.curr.execute("""create table 35mmc_raw(
            title text,
            url text,
            raw_text text
        )""")
        print("Done Table.")

    def store_db(self, title, url, raw_text):
        self.curr.execute(
            """INSERT INTO {} (title, url, raw_text) VALUES (%s, %s, %s)""".format(self.table_name),
            (title, url, raw_text)
        )
        self.conn.commit()  
        

if __name__ == '__main__':
    start_url = 'https://www.35mmc.com/14/10/2021/pentax-iqzoom-928-review/'
    db = databasePipeline('localhost', 'root', 'aingg', '35mmc', '35mmc_raw')
    start_level = 1 
    crawl_3level(db, start_url, start_level)           