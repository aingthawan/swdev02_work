import requests
import bs4
import pandas as pd

title_list = []
url_list = []

print("\nStarting . . .")

data = requests.get("https://pantip.com/tag/Backpack")
soup = bs4.BeautifulSoup(data.text, "html.parser")

title = soup.find_all('h2')

for i in title:
    # extract a
    a_tag = i.find('a')
    # print title
    title_list.append(a_tag.text)
    # print link
    url_list.append(a_tag['href'])

table = pd.DataFrame([title_list, url_list]).transpose()
print(table)

print("End\n")