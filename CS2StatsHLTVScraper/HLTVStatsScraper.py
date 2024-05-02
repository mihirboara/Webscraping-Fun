# HLTV Stats Scraper
''' 
Things to possibly add:
- Option to send to DB instead of csv
- More filtering options i.e. instead of Top50 can choose Top30/20/10, more date range options, different cs versions(GO or 2), etc.
- Team's player/coach rosters
- Player stats
- 
'''

import time
import pandas as pd
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from datetime import datetime
from dateutil.relativedelta import relativedelta


# Set variables for stats URL (Team Overview Page by Default)
HLTVBaseURL = 'https://www.hltv.org'
Version = '?csVersion=CS2'
FTUPageAddon = '/ftu'
PistolsPageAddon = '/pistols'
HLTVStatsPageURLAddon = '/stats/teams'
# Set variables for date filters (Last 12 Months)
StartDate = (datetime.today() - relativedelta(years=1)).strftime('%Y-%m-%d')
EndDate = datetime.today().strftime('%Y-%m-%d')
HLTVDateFilter = '&startDate=' + StartDate + '&endDate=' + EndDate

# Set variables for team ranking filters (Top 50)
Top50Ranking = 'Top50'
HLTVRankingFilter = '&rankingFilter=' + Top50Ranking
# print(HLTVBaseURL + HLTVStatsPageURLAddon + HLTVDateFilter + HLTVRankingFilter)

# Start an undetected chrome instance and go to Team Overview Stats page
driver = uc.Chrome()
driver.get(HLTVBaseURL + HLTVStatsPageURLAddon + Version + HLTVDateFilter + HLTVRankingFilter)
print('Overview URL:\n' + HLTVBaseURL + HLTVStatsPageURLAddon + Version + HLTVDateFilter + HLTVRankingFilter)


# Select Cookie Preference
time.sleep(2)
driver.find_element(By.ID, 'CybotCookiebotDialogBodyButtonDecline').click()
time.sleep(2)

# Get the countries/place the teams are based out of i.e. Ukraine, Europe, North America, France, etc, storing them into a list.
TopTeamsLocationList = []
flags = driver.find_elements(By.TAG_NAME, 'img')
i=0
for flag in flags:
    if(flag.get_attribute('class') == 'flag'):
        TopTeamsLocationList.append(flag.get_attribute('title'))
        i+=1
TopTeamsLocationList = [w.replace('Other', 'International') for w in TopTeamsLocationList]
TopTeamsLocationListSeries = pd.Series(TopTeamsLocationList)

# Get the top 50 teams and their specific pages on HLTV, storing them into a list.
TopTeamsList = []
lnks=driver.find_elements(By.TAG_NAME, 'a')
i=0
for link in lnks:
    showlink = link.get_attribute('href')
    if(i==47):
        break
    if(type(showlink) is str):
        if('https://www.hltv.org/stats/teams/' in showlink[:33]):
            TopTeamsList.append([showlink,showlink[33:-74].split('/')])
            i+=1


# Locate and create a dataframe of the team overview stats table, then output to a csv file
TeamStatsTableElem = driver.find_element(By.XPATH, '/html/body/div[2]/div[5]/div[2]/div[1]/div[2]/table')
TeamStatsOverviewDF = pd.read_html(TeamStatsTableElem.get_attribute('outerHTML'))
TeamStatsOverviewDF[0].insert(loc=2, column='Org Location', value=TopTeamsLocationListSeries)
TeamStatsOverviewDF[0].to_csv('TeamOverviewStats.csv', index=True)
time.sleep(3)


# Go to Team FTU Stats page
# print('FTU URL:\n' + HLTVBaseURL + HLTVStatsPageURLAddon + Version + FTUPageAddon + HLTVDateFilter + HLTVRankingFilter)
driver.get(HLTVBaseURL + HLTVStatsPageURLAddon + FTUPageAddon + Version + HLTVDateFilter + HLTVRankingFilter)

# Locate and create a dataframe of the team FTU stats table, then output to a csv file
TeamStatsTableElem = driver.find_element(By.XPATH, '/html/body/div[2]/div[5]/div[2]/div[1]/div[2]/table[1]')
TeamStatsFTUDF = pd.read_html(TeamStatsTableElem.get_attribute('outerHTML'))

# Read the previously created csv file and remove the unecessary header row and rewrite to the csv file
TeamStatsFTUDF[0].to_csv('TeamFTUStats.csv', index=True)
df = pd.read_csv('TeamFTUStats.csv', skiprows=1)
df.to_csv('TeamFTUStats.csv', index=False)
time.sleep(3)


# Go to Team Pistols Stats page
# print('Pistols URL:\n' + HLTVBaseURL + HLTVStatsPageURLAddon + Version + PistolsPageAddon + HLTVDateFilter + HLTVRankingFilter)
driver.get(HLTVBaseURL + HLTVStatsPageURLAddon + PistolsPageAddon + Version + HLTVDateFilter + HLTVRankingFilter)

# Locate and create a dataframe of the team Pistols stats table, then output to a csv file
TeamStatsTableElem = driver.find_element(By.XPATH, '/html/body/div[2]/div[5]/div[2]/div[1]/div[2]/table')
TeamStatsPistolsDF = pd.read_html(TeamStatsTableElem.get_attribute('outerHTML'))
TeamStatsPistolsDF[0].to_csv('TeamPistolsStats.csv', index=True)
time.sleep(3)




time.sleep(5)
