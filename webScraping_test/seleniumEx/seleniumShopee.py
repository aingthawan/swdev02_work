from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import bs4
import time
import pandas as pd
import os

# function to open and navigate page to specific keyword
def openShopee(inputKeyword):
    # open chrome window
    driver = webdriver.Chrome()
    # go to shopee.com
    driver.get('https://shopee.co.th/')
    # navigate to thai lang button and click
    thai_button = driver.find_element('xpath', '/html/body/div[2]/div[1]/div[1]/div/div[3]/div[1]/button')
    thai_button.click()
    # summon javascript, querySelector : get info of the button location
    # eliminate shadowRoot, close popup
    close_button = driver.execute_script('return document.querySelector("shopee-banner-popup-stateful").shadowRoot.querySelector("div.shopee-popup__close-btn")')
    close_button.click()
    # enter navigate, keywords and search
    search_bar = driver.find_element('xpath', '/html/body/div[1]/div/header/div[2]/div/div[1]/div[1]/div/form/input')
    search_bar.send_keys(inputKeyword)
    search_bar.send_keys(Keys.ENTER)
    # zoom out to 10% webpage to load all product
    # using javascript command
    driver.execute_script("document.body.style.zoom='10%'")
    # return html data
    time.sleep(5)
    raw_data = driver.page_source
    driver.close();
    return raw_data

# extract to output pandas table
def shopeeExtracttoTable(rawData):
    prefix = 'https://shopee.co.th/'
    productNameList = []
    productPriceList = []
    productURLList = []
    retailerLocationList = []
    saleCountList = []

    soup = bs4.BeautifulSoup(rawData, "html.parser")
    separateProduct = soup.find_all('div', {'class':'col-xs-2-4 shopee-search-item-result__item'})
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

    return dataTable

# output panda s table as JSON
def exportTable(outputDataframe, filepath, fileName):
    print("Saved to : ", filepath + '\\' + fileName + "_ScrapResults")
    # outputDataframe.to_csv(filepath + '\\' + fileName + "_ScrapResults")
    outputDataframe.to_csv(filepath + '\\' + fileName + "_ScrapResults.csv")

# main code
def main():
    print("\nStart Scraping SHOPEE . . .")
    toSearch = 'หม้อทอดไร้น้ำมัน'
    Results = shopeeExtracttoTable(openShopee(toSearch))
    print('Exporting . . .')
    exportTable(Results, os.getcwd(), toSearch)
    print("End Program.\n")


if __name__ == "__main__":
    main()
