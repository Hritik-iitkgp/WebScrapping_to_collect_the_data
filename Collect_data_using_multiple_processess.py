from bs4 import BeautifulSoup
import urllib
from urllib.request import urlopen
import sqlite3
import json
import random

def createDatabaseConnect(dbName):
	con = sqlite3.connect(dbName)
	cur = con.cursor()
	return cur , con


url = "https://en.wikipedia.org/wiki/Summer_Olympic_Games"
html = urlopen(url)
SummerOlympics = html.read()
soup = BeautifulSoup(SummerOlympics, 'html.parser')
tables = soup.find_all('table',attrs={'class':'sortable'})
i=1
links=[]
for row in tables[1].tbody.findAll('tr'):
    if(i>2):
        link = row.findAll('td')
        if(len(link)>=2):
            links.append(link[1].a['href'])
    i+=1
urls=[]
for i in links:
    if(int(i.split('/')[2].split('_')[0])<1968 or int(i.split('/')[2].split('_')[0])>2020):
        links.remove(i)
    else:
        urls.append(i)
links=urls
#use random.sample for random sampling to find the possible links and run it all processing through multiple processess

samples=['/wiki/1976_Summer_Olympics', '/wiki/2016_Summer_Olympics', '/wiki/2008_Summer_Olympics', '/wiki/1972_Summer_Olympics', '/wiki/2004_Summer_Olympics', '/wiki/1984_Summer_Olympics', '/wiki/2020_Summer_Olympics', '/wiki/2012_Summer_Olympics', '/wiki/2000_Summer_Olympics', '/wiki/1988_Summer_Olympics']

#For each of the pages of your two selected summer olympics, extract the data
#Name, WikipediaURL, Year, HostCity, ParticipatingNations, Atheletes, Sports, Rank_1_nation, Rank_2_nation, Rank_3_nation

# create table and store the details
dbName = "OlympicsData.db"
cursor,con = createDatabaseConnect(dbName)

# table to store the details of summer olympics
query = "CREATE TABLE IF NOT EXISTS SummerOlympics(id INTEGER PRIMARY KEY AUTOINCREMENT,Name, WikipediaURL, Year,HostCity,Athletes,Rank_1_nation,Rank_2_nation,Rank_3_nation,nation,done)"
cursor.execute(query)

# table to store the list of countries participating
query = "CREATE TABLE IF NOT EXISTS Countries(c_id INTEGER NOT NULL,Name,FOREIGN KEY (c_id) REFERENCES SummerOlympics (id))"
cursor.execute(query)

# table to store the list of sports
query = "CREATE TABLE IF NOT EXISTS sports(s_id INTEGER NOT NULL,Name,FOREIGN KEY (s_id) REFERENCES SummerOlympics (id))"
cursor.execute(query)


# using beautiful soup parse the 
url = "https://en.wikipedia.org"
m=1
ranks_of_nations=[]
for i in samples:
    url1=url+i
    query = "INSERT INTO SummerOlympics VALUES ('%d','%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s','%s','%d')"%(m,'',url1,'','','','','','','',0)
    cursor.execute(query)
    con.commit()
    m+=1
import os
for i in range(3):
    os.system("python3 scrapper.py &")


