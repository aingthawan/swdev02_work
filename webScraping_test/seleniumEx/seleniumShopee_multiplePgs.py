from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import bs4
import time
import pandas as pd
import os

# function to open and navigate page to specific keyword
def openShopee(inputKeyword, pageRange):
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

    driver.execute_script("document.body.style.zoom='10%'")
    for i in range(pageRange):
        print("Getting Page ", i+1, " of ", pageRange)
        time.sleep(4)
        shopeeExtracttoList(driver.page_source)
        nextPageShopee(driver)  

# turn to next shopee page
def nextPageShopee(driver):
    driver.execute_script("document.body.style.zoom='100%'")
    nextButton = driver.find_element('xpath', '/html/body/div[1]/div/div[2]/div/div/div[2]/div[3]/div[3]/div/button[8]')
    nextButton.click()
    driver.execute_script("document.body.style.zoom='10%'")

# extract data to list
def shopeeExtracttoList(rawData):
    prefix = 'https://shopee.co.th/'

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

# get list and return pandas table
def makeTable():
    dataFrame = pd.DataFrame([
        productNameList, 
        productPriceList, 
        saleCountList, 
        retailerLocationList, 
        productURLList
    ]).transpose()
    dataFrame.columns = ['Product Name', 'Price', 'Item Sale', 'Retailer Location', 'Product URL']
    return dataFrame

# output panda s table as JSON
def exportFile(outputDataframe, filepath, fileName):
    goto = filepath + '\\' + fileName + "_ScrapResults.csv"
    outputDataframe.to_csv(goto)
    print("Saved to : ", goto)

# main code
def main():
    print("\nStart Scraping SHOPEE . . .")
    toSearch = 'mask'
    print("Keyword : ", toSearch)
    pageToScrap = 10

    openShopee(toSearch, pageToScrap)

    # finalData = makeTable()
    print("Exporting")
    exportFile(makeTable(), os.getcwd(), toSearch.replace(" ",'') + '_' + str(pageToScrap) + "Pages")
    print("End Program. \n")

if __name__ == "__main__":
    productNameList = []
    productPriceList = []
    productURLList = []
    retailerLocationList = []
    saleCountList = []

    main()
