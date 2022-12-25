import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from tqdm import tqdm

def dpReviewExtract(url):
    camName = [] 
    shortInfo = [] 
    dateRel = []
    ovURL = []
    rvURL = []
    
    web_request = requests.get(url)
    soup = BeautifulSoup(web_request.text, "html.parser")
    all_body = soup.find_all('td', {'class':'product'})
    for i in all_body:
        # extract camera name
        cameraName = i.find('div', {'class':'info'}).find('div', {'class':'name'}).find('a').text
        releaseDate = i.find('div', {'class':'info'}).find('div', {'class':'announcementDate'}).text
        
        try:
            shortSpecs = i.find('div', {'class':'info'}).find('div', {'class':'specs'}).text
        except AttributeError:
            shortSpecs = None
            
        try:
            overviewURL = i.find('div', {'class':'info'}).find('div', {'class':'name'}).find('a')['href']
        except AttributeError:
            overviewURL = None
        
        try:
            previewURL = i.find('div', {'class':'info'}).find('div', {'class':'review'}).find('a')['href']
        except AttributeError:
            previewURL = None
        
        camName.append(cameraName)
        dateRel.append(releaseDate)
        shortInfo.append(shortSpecs)
        ovURL.append(overviewURL)
        rvURL.append(previewURL)
        
    return infoToDataframe(camName, shortInfo, dateRel, ovURL, rvURL)
        
def infoToDataframe(name, info, date, overview, preview):
    dataFrame = pd.DataFrame([name, info, date, overview, preview]).transpose()
    dataFrame.columns = ['CameraName', 'Info', 'Date Release', 'Overview URL', 'Preview URL']
    return dataFrame

def exportFile(outputDataframe, fileName):
    print("Exporting . . .")
    goto = os.getcwd() + '\\webScraping_test\\soupDpreview\\' + fileName
    outputDataframe.to_csv(goto)
    print(end="\r")
    print("Saved to : ", goto)




def main():
    outputDataframe = pd.DataFrame({})
    url = 'https://www.dpreview.com/products/cameras/all?page='
    pageRange = 50

    print("\nStarting . . . ")
    for i in tqdm(range(pageRange)):
        print(end="\r")
        outputDataframe = pd.concat([outputDataframe, dpReviewExtract(url + str(i+1))])
    
    exportFile(outputDataframe, 'dpReviewExtract.csv')
    print("End Program.\n")
        
        
if __name__ == "__main__":
    main()
