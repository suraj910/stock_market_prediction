import urllib

from bs4 import BeautifulSoup
import requests
import re
from datetime import date
from datetime import datetime, timedelta

date_today = date.today()
date_yestarday = date.today() - timedelta(1)

url = f"https://www.indiainfoline.com/markets/live-news/{date_today}/Live-News-Sensex-Nifty-live-stock-markets-bse-nse-futures-and-options-derivative-trading"

news = requests.get(url)
doc = BeautifulSoup(news.text, "html.parser")


headings = list()
for updates in doc.find_all("h2", attrs={"class": "fw500 fs20e blue_text"}):    # GET ALL HEADINGS IN TEXT STORED IN LIST
   headings.append(updates.text)

# print("UPDATES = ", headings)

links = doc.find("div", attrs={"class": "story_card h_auto"})   # GET ALL STORY CARDS (UPDATES) FROM THE PAGE

click_link = list()
for l in links.find_all('a', attrs={'href': re.compile("^https://")}):  # EXTRACT LINKS FROM THE STORY CARDS
    if l.get('href').endswith('html'):
        click_link.append(l.get('href'))


# print("LINKS = ", click_link)

headings_links = dict(zip(headings, click_link))    # TEXT AND LINKS COMBINED INTO A DICTIONARY
limitedIifl = dict(list(headings_links.items())[:25])

if __name__ == "__main__":
    print(limitedIifl)




