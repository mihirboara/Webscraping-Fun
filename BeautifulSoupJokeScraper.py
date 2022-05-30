# Beautiful Soup Messing Around

import random
import requests
from bs4 import BeautifulSoup

def getdata(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    r = requests.get(url, headers=headers)
    return r.text

url = "https://pun.me/jokes/dad/"

htmldata = getdata(url)
soup = BeautifulSoup(htmldata, 'html.parser')
    
jokes = []
for item in soup.find_all("ul", class_="puns"):
    tempJokes = item.get_text().split("\n")
    for i in range(len(tempJokes)):
        if(tempJokes[i] != ""):
            jokes.append(tempJokes[i])

# print(jokes)
# print("-------------------------------")
print(random.choice(jokes).strip())
