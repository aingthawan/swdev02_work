# Aing K.
# Test Porsche Web Scraping with Python

import requests
from bs4 import BeautifulSoup

url = "https://www.porsche.com/pap/_thailand_/models/911/"
web_data = requests.get(url)

soup = BeautifulSoup(web_data.text, "html.parser")
# find_word = soup.find_all("div", {"class": "m-14-model-name"})
find_word = soup.find_all("div", {"class": "m-14-model-name"})

for i in find_word:
    
    print(i)