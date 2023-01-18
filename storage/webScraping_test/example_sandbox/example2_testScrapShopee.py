# Aing K.
# Test Porsche Web Scraping with Python
# REMARK !!!!!
# this method not work with shopee!!!

import requests
from bs4 import BeautifulSoup
import pandas as pd

# url = "https://www.porsche.com/pap/_thailand_/models/911/"
url = "https://shopee.co.th/search?keyword=%E0%B8%AB%E0%B8%A1%E0%B9%89%E0%B8%AD%E0%B8%AA%E0%B8%99%E0%B8%B2%E0%B8%A1&page=0"
web_data = requests.get(url)

soup = BeautifulSoup(web_data.text, "html.parser")
separateProduct = soup.find_all('div', {'class':'col-xs-2-4 shopee-search-item-result__item'})
# find_word = soup.find_all("div", {"class": "m-14-model-price"})

print(separateProduct)

# for i in find_word:
#     # spit the string
#     print(i)
#     i = str(i).split('<div class="m-14-model-price">')[1]
#     print(i)
#     # spit the string
#     i = str(i).split('</div>')[0]
#     print(i)

prefix = 'https://shopee.co.th/'
productNameList = []
productPriceList = []
productURLList = []
retailerLocationList = []
saleCountList = []

for stuff in separateProduct:
        productNameList.append(stuff.find('div', {'class':'ie3A+n bM+7UW Cve6sh'}).text)
        productPriceList.append(stuff.find('div',{'class':'vioxXd rVLWG6'}).text)
        if (stuff.find('div',{'class':'r6HknA uEPGHT'}) != None):
            saleCountList.append(stuff.find('div',{'class':'r6HknA uEPGHT'}).text)
        else:
            saleCountList.append("No Sale")
        productURLList.append(prefix + stuff.find('a')['href'])
        retailerLocationList.append(stuff.find('div', {'class':'zGGwiV'}).text)

dataTable = pd.DataFrame([
    productNameList, 
    productPriceList, 
    saleCountList, 
    retailerLocationList, 
    productURLList
]).transpose()

dataTable.columns = ['Product Name', 'Price', 'Item Sale', 'Retailer Location', 'Product URL']

print(dataTable)