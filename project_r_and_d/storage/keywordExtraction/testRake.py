from rake_nltk import Rake
import requests
from bs4 import BeautifulSoup
import spacy

# instance for rake obj.
r = Rake()

web_req = requests.get("https://www.35mmc.com/21/12/2018/canon-ql17-giii-review/")

soup = BeautifulSoup(web_req.text, "html.parser")
# print(soup)
articleBody = soup.find('article')
print(soup.find('div', {'class':'entry-content'}))


# r.extract_keywords_from_text(articleBody)

# # save r.get_ranked_phrases_with_scores() to text file
# with open('rakeTest.txt', 'w') as f:
#     for item in r.get_ranked_phrases_with_scores():
#         f.write(str(item))
# f.close()
        
    
