import requests
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from PIL import Image

# Reading Auth info from separate txt file
with open('RedditAPIInfo.txt', 'r') as f:
    info = f.readlines()
    CLIENT_ID = info[2].strip()
    SECRET_KEY = info[4].strip()
    username = info[6].strip()
    password = info[8].strip()

# Authentication
auth = requests.auth.HTTPBasicAuth(CLIENT_ID, SECRET_KEY)
data = {'grant_type':'password', 'username':username, 'password':password}
headers = {'User-Agent':'testingAPI/0.0.1'}
res = requests.post('https://www.reddit.com/api/v1/access_token', 
                    auth=auth, data=data, headers=headers)
TOKEN = res.json()['access_token']
headers['Authorization'] = f'bearer {TOKEN}'
# Not necessary, resets every ~2 hours apparently tho
# requests.get('https://oauth.reddit.com/api/v1/me', headers=headers)

# Get input from user for which subreddit and which category of posts to request
subRedd = input("Enter the subreddit name: ")

catChoice = input("Enter 1 for Top, 2 for Hot, 3 for New and 4 for Rising: ")
category = ""
if catChoice == 1:
    category = "Top"
if catChoice == 2:
    category = "Hot"
if catChoice == 3:
    category = "New"
if catChoice == 4:
    category = "Rising"

reddRequest = "https://oauth.reddit.com/r/" + subRedd + "/" + category

# Request data from Reddit for the wordcloud
res = requests.get(reddRequest, headers=headers)
text = ""
for post in res.json()['data']['children']:
    text = text + post['data']['title'] + " "

# Can add more stopwords to exclude from the wordclouds if needed
stop_words = list(STOPWORDS) + ["having", "using", "used", "with"]

# Create the wordcloud
mask = np.array(Image.open("redditLogo.png"))
wordcloud = WordCloud(mask=mask,contour_color='#ff4500',contour_width=3,
                    colormap='autumn', collocations=False,stopwords=stop_words).generate(text)

# Display the generated wordcloud image:
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()