from cleanRawText import TextCleaner
from singleScrape import pageScraper
import pandas as pd
import os
import csv

# function to check if a URL already exists in the file
def check_url(file_path, url):
    # open the CSV file for reading
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        # iterate through the rows in the file
        for row in reader:
            # check if the URL already exists in the file
            if row['url'] == url:
                return True
    return False

# function to insert a new row into the file
def insert_row(file_path, new_row):
    # open the CSV file for reading
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        # create a list to store the existing rows
        rows = []
        # iterate through the rows in the file
        for row in reader:
            # add the row to the list
            rows.append(row)
    # add the new row to the list of existing rows
    rows.append(new_row)

    # open the CSV file for writing
    with open(file_path, 'w', newline='') as file:
        fieldnames = ['id', 'url']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        # write the header row
        writer.writeheader()
        # write all the rows to the file
        for row in rows:
            writer.writerow(row)

def get_last_id(file_path):
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        last_id = 0
        for row in reader:
            last_id = row["id"]
        return last_id            

def web_crawler(url, current_level=0):
    if check_url(file_path, url) == False:
        # retrieve data from current url
        data = ps.scrape_page(url)
        # get the raw text
        raw_text = data['rawText']
        keywords = tc.clean(raw_text)
        # get the backlinks
        backlinks = data['backlinks']
        CurrentID += 1
        insert_row(file_path, {'id': CurrentID, 'url': url})
    # print(keywords, backlinks)
    # if current level is less than 3
    if current_level < 3:
        # recursively call the web_crawler function on each backlink
        for link in backlinks:
            web_crawler(link, current_level+1)



dir_path = 'project/honmono/'
file_name = 'webData.csv'
file_path = dir_path + file_name

CurrentID = get_last_id('ScrapeDataStatus.py')

tc = TextCleaner()
ps = pageScraper()

# check if webData.csv exists
if os.path.exists(file_path) == False:
    df_webData = pd.DataFrame(columns=['id', 'url'])
    df_webData.to_csv(file_path, index=False)

web_crawler('https://www.35mmc.com/17/01/2023/the-digital-rangefinder-an-endangered-species-by-ailbiona-mclochlainn/', 4)

# new_row = {'id': 11, 'url': 'https://www.35mmc.com/17/01/2023/the-digital-rangefinder-an-endangered-species-by-ailbiona-mclochlainn/'}

# # check if the URL already exists in the file
# if check_url(file_path, new_row['url']):
#     print('URL already exists in file')
# else:
#     # insert the new row into the file
#     insert_row(file_path, new_row)

# update ScrapeDataStatus
with open("ScrapeDataStatus.py", "w") as f:
    f.write("CurrentID = " + str(CurrentID))
