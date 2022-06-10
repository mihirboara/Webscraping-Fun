import tweepy
import re
import matplotlib.pyplot as plt
import textblob
from textblob import TextBlob
from cleantext import clean

# Reading Auth info from separate txt file
with open('TwitterAPIInfo.txt', 'r') as f:
    info = f.readlines()
    CLIENT_ID = info[2].strip()
    CLIENT_SECRET = info[4].strip()
    CONSUMER_KEY = info[6].strip()
    CONSUMER_SECRET = info[8].strip()
    BEARER_TOKEN = info[10].strip()
    ACCESS_TOKEN = info[12].strip()
    ACCESS_TOKEN_SECRET = info[14].strip()
    username = info[16].strip()
    password = info[18].strip()

# print(CLIENT_ID, SECRET_KEY, BEARER_TOKEN, ACCESS_TOKEN, ACCESS_TOKEN_SECRET, username, password)

# Get user input on what topic to search for and the number of resulting tweets to analyze
userInput = input("What topic would you like to search: ")
queryInput = userInput + ' lang:en -is:retweet'
maxResults = input("How many tweets would you like to use (10-100 Only): ")

# Access the tweets selected using the Tweepy API
client = tweepy.Client(BEARER_TOKEN)
tweets = client.search_recent_tweets(query=queryInput, max_results=maxResults)

# Clean up the tweets acquired
cleanedTweets = []
for tweet in tweets.data:
    # print(tweet.text)
    cleanishTweet = (clean(tweet.text, no_emoji=True, 
        fix_unicode=True, to_ascii=True, no_urls=True,
        no_emails=True, no_phone_numbers=True))
    cleanedTweets.append(' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", cleanishTweet).split()))

# Run sentiment analysis on each tweet and update vars based on positivity, negativity or neutrality
negCount = 0
posCount = 0
neuCount = 0
polarities = []
for tweet in cleanedTweets:
    analysis = TextBlob(tweet)
    # print(analysis.sentiment.polarity)
    polarities.append(analysis.sentiment.polarity)
    if analysis.sentiment.polarity > 0:
        posCount+=1
    elif analysis.sentiment.polarity < 0:
        negCount+=1
    else:
        neuCount+=1

# Print out each tweet and its respective polarity
print("\n-------------- Tweets For \'" + userInput + "\' --------------")
for i in range(len(cleanedTweets)):
    print(str(i+1) + " -Polarity of " + str(polarities[i]) + "- " + cleanedTweets[i])
print("\n")

# Print out the sentiment analysis stats for the tweets, the polarities and the percentages of pos, neg and neutral 
posPercent = round((posCount/int(maxResults))*100, 2)
negPercent = round((negCount/int(maxResults))*100, 2)
neuPercent = round((neuCount/int(maxResults))*100, 2)
print("------------ Polarities For \'" + userInput + "\' ------------")
print(polarities)
print("\n" + "------------ Percentages ------------")
print("Percentage Positive: " + str(posPercent) + "%" + " (" + str(posCount) + "/" + maxResults + ")")
print("Percentage Negative: " + str(negPercent) + "%" + " (" + str(negCount) + "/" + maxResults + ")")
print("Percentage Neutral: " + str(neuPercent) + "%" + " (" + str(neuCount) + "/" + maxResults + ")")
print("\n")

# Generate a pie chart displaying the sentiment percentages
myLabels = ["Positive " + str(posPercent) + "%", "Negative " + str(negPercent) + "%", "Neutral " + str(neuPercent) + "%"]
sizes = [posPercent, negPercent, neuPercent]
myColors = ["#1da1f2", "#14171a", "#657786"]
fig1, ax1 = plt.subplots()
plt.pie(sizes, labels=myLabels, colors=myColors)
plt.title("Twitter User Sentiments for \'" + userInput + "\'")
plt.show()