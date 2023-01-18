# Aing K.
# Test Web Scraping with Python

import requests
from bs4 import BeautifulSoup

url = "https://www.borntodev.com/online-course/"
web_data = requests.get(url)

soup = BeautifulSoup(web_data.text, "html.parser")
find_word = soup.find_all("h2", {"class": "woocommerce-loop-product__title"})

for i in find_word:
    i = str(i).split('<h2 class="woocommerce-loop-product__title">')[1]
    i = str(i).split('</h2>')[0]
    print(i)

