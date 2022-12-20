# Aing K.
# Test Porsche Web Scraping with Python

import requests
from bs4 import BeautifulSoup

url = "https://www.porsche.com/pap/_thailand_/models/911/"
web_data = requests.get(url)

soup = BeautifulSoup(web_data.text, "html.parser")
# 
find_word = soup.find_all("div", {"class": "m-14-model-price"})

for i in find_word:
    # spit the string
    i = str(i).split('<div class="m-14-model-price">')[1]
    # spit the string
    i = str(i).split('</div>')[0]
    print(i)