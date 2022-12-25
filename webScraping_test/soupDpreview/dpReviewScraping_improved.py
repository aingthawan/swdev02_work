# Optimized version of dpReviewScraping.py
# To do parallel scraping
# Faster for sure!, Trust me bro.

import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from tqdm import tqdm
import concurrent.futures

# Open input dp review url and extract to table ( pandas dataFrame )
def dpReviewExtract(url):
    camName = [] 
    shortInfo = [] 
    dateRel = []
    ovURL = []
    rvURL = []
    mpxl = [] 
    # request html from target
    web_request = requests.get(url)
    # create bs object
    soup = BeautifulSoup(web_request.text, "html.parser")
    # separate each product
    all_body = soup.find_all('td', {'class':'product'})
    # loop for extract desired information an append to list
    for i in all_body:
        # extract camera name
        cameraName = i.find('div', {'class':'info'}).find('div', {'class':'name'}).find('a').text
        # extract release date
        releaseDate = i.find('div', {'class':'info'}).find('div', {'class':'announcementDate'}).text.split('Announced ')[1]
        # extract short information
        try:
            specTemp = i.find('div', {'class':'info'}).find('div', {'class':'specs'}).text
            # get megapixels
            megapixels = specTemp.split(' megapixels ')[0]
            # get other info
            shortSpecs = specTemp.split(' | ')[1:]
        except AttributeError:
            shortSpecs = None
        # extract overview URL
        try:
            overviewURL = i.find('div', {'class':'info'}).find('div', {'class':'name'}).find('a')['href']
        except AttributeError:
            overviewURL = None
        # extract Review URL
        try:
            previewURL = i.find('div', {'class':'info'}).find('div', {'class':'review'}).find('a')['href']
        except AttributeError:
            previewURL = None
        # Append to list
        camName.append(cameraName)
        dateRel.append(releaseDate)
        shortInfo.append(shortSpecs)
        ovURL.append(overviewURL)
        rvURL.append(previewURL)    
        mpxl.append(megapixels)
    # call function for turing lists to pandas dataFrame
    return infoToDataframe(camName, mpxl, shortInfo, dateRel, ovURL, rvURL)
        
# function for turing lists to pandas dataFrame, get called from dpReviewExtract       
def infoToDataframe(name, megapix,info, date, overview, preview):
    dataFrame = pd.DataFrame([name, megapix, info, date, overview, preview]).transpose()
    dataFrame.columns = ['CameraName', 'Megapixels', 'Info', 'Date Release', 'Overview URL', 'Preview URL']
    return dataFrame

# exporting dataFrame to csv file
def exportFile(outputDataframe, fileName):
    print("Exporting . . .")
    goto = os.getcwd() + '\\webScraping_test\\soupDpreview\\' + fileName
    outputDataframe.to_csv(goto)
    print("Saved to : ", goto)

# main code
def main():
    outputDataframe = pd.DataFrame({})
    url = 'https://www.dpreview.com/products/cameras/all?page='
    pageRange = 50
    print("\nStarting . . . ")
    # Use a ThreadPoolExecutor to execute the scraping tasks separately (parallel scraping)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Start a list of tasks to be executed separately
        tasks = [executor.submit(dpReviewExtract, url + str(i+1)) for i in range(pageRange)]
        # Use tqdm to display a progress bar, Iterate oner a completed task
        for task in tqdm(concurrent.futures.as_completed(tasks), total=len(tasks)):
            # gathering output
            outputDataframe = pd.concat([outputDataframe, task.result()])
    # exporting csv file
    exportFile(outputDataframe, 'dpReviewExtract_50pages.csv')
    print("End Program.\n")
        
        
if __name__ == "__main__":
    main()