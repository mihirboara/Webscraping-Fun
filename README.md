# Webscraping-Fun
Messing around with various small projects to learn more about web scraping.

So far there is:

A Bad Joke Generator, using BeautifulSoup to scrape a website for bad jokes and selecting one at random to output.

A Reddit API Wordcloud script that allows you to input a subreddit and the category(Top, Rising, etc.) and generates a wordcloud from the titles gotten from the selections, using the Reddit API.

A Twitter API Sentiment Analyzing script that allows you to input a keyword to search on and number of tweets (between 10 and 100) to use in the sentiment analysis, then prints the tweets with their respective polarities, the percentages of positive, negative and neutral tweets for the given keyword and displays a pie chart of those percentages. Uses Textblob, MatPlotLib, re, Clean-Text and Tweepy.

A CS2 Stats script that scrapes the HTML of HLTV.org, a website that aggregates stats for players, teams, and matches for popular esports title 'Counter-Strike'. The script at this point specifically scrapes team data for the most recent iteration of the Counter-Strike series, 'Counter-Strike 2', for the top 50 teams in the last 12 months. Uses primarily the Selenium and Pandas libraries, and outputs the data to CSV files. These CSV files were used by me for a Tableau Dashboard project that can be found [here](https://public.tableau.com/app/profile/mihir.boara/viz/CS2StatsDashboard/Dashboard1).
