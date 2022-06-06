import requests
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

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

# Request data from Reddit and create the wordcloud from the title texts
res = requests.get(reddRequest, headers=headers)
text = ""
for post in res.json()['data']['children']:
    text = text + post['data']['title'] + " "

wordcloud = WordCloud().generate(text)

# Display the generated image:
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()