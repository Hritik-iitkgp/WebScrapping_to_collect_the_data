# TASK : collect  summer olympics data from its Wikipedia page and
#  process it using Python's urllib3 , requests and BeautifulSoup library and store the collected information in a SQLite database.

# STEPS :
# --  Collect the data from, https://en.wikipedia.org/wiki/Summer_Olympic_Games .
# --  Create a database Create aSQLite database named 'OlympicsData.db' and a table
#  named'SummerOlympics' with the respective columns
# -- Fetch the HTML data from the webpage that lists information about the Summer Olympics.
# -- Analyze the HTML structure to identify the sections or elements containing the URLs of individual Summer Olympics wiki pages.
# -- Utilize parsing techniques, such as using libraries like BeautifulSoup in Python, to extract these URLs.
# -- Apply filtering criteria to select the URLs corresponding to two random Olympics that occurred within the last 50 years (from 1968 to 2020).
# -- Output or store these selected URLs for further processing or analysis.
# --  For each of the pages of your two selected summerolympics, extract the data (with the help
#  of BeautifulSoup) mentioned in step 2 and insert in the database


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
# whenever we request for any website it will return the normal html file which is completely unstructured
url = "https://en.wikipedia.org/wiki/Summer_Olympic_Games"
html = urlopen(url)
SummerOlympics = html.read()
# so to collect information from such sources we use python library bs4 (beautiful soup which is desined to process the html and others) 
soup = BeautifulSoup(SummerOlympics, 'html.parser')
## As per Required task we need to scrap the three columns Name, WikipediaURL, Year, HostCity, ParticipatingNations, Atheletes, Sports, Rank_1_nation, Rank_2_nation, Rank_3_nation
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
samples=random.sample(links, 2)	

# create table and store the details
dbName = "OlympicsData.db"
cursor,con = createDatabaseConnect(dbName)

# table to store the details of summer olympics
query = "CREATE TABLE IF NOT EXISTS SummerOlympics(id INTEGER PRIMARY KEY AUTOINCREMENT,Name, WikipediaURL, Year,HostCity,Athletes,Rank_1_nation,Rank_2_nation,Rank_3_nation,nation)"
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
## we will parse the and store these, WikipediaURL, Year, HostCity, ParticipatingNations, Atheletes, Sports, Rank_1_nation, Rank_2_nation, Rank_3_nation  
# as structured data for all the pages
for i in samples:
    html = urlopen(url+i)
    list_countries=[]
    list_sports=[]
    specificGame = html.read()
    soup = BeautifulSoup(specificGame, 'html.parser')
    details=soup.find_all('td',attrs={'class':'infobox-data'})
    name=soup.find('span',attrs={'class':'mw-page-title-main'}).text
    year=name.split()[0]
    url1=url+i
    hostCity=details[0].text.split(',')[0]
    nation=soup.find('th',string='Nations').find_next('td').text.split()[0].strip()
    no_of_athelete=soup.find('th',string='Athletes').find_next('td').text.strip()
    tables = soup.find('table',attrs={'class':'plainrowheaders'}).find('tbody').find_all('tr')
    rank1=tables[1].find('th').a.text
    rank2=tables[2].find('th').a.text
    rank3=tables[3].find('th').a.text
    listofnations = soup.find('span',string='Participating National Olympic Committees').find_next('table').find_all('li')
    ranks_of_nations.append(set([rank1,rank2,rank3]))
    for j in listofnations:
        if(j.a.text!=""):
            query="INSERT INTO Countries VALUES ('%d','%s')"%(m,j.a.text.strip())
            cursor.execute(query)
    query = "INSERT INTO SummerOlympics VALUES ('%d','%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s','%s')"%(m,name,url1,year,hostCity,no_of_athelete,rank1,rank2,rank3,nation)
    cursor.execute(query)
    m+=1
query = "SELECT * from SummerOlympics"
result = cursor.execute(query)
print("list of choosen years",end=': ')
sum=0
for row in result:
	print(row[3],end=' ')
print()
query = "SELECT count(*) as sum from Countries"
result = cursor.execute(query)
for row in result:
    print("Average number of countries participating in the two olympics",row[0]//2)

print("overlap within <Rank_1_nation, Rank_2_nation and Rank_3_nation> for chosen two years",ranks_of_nations[0].intersection(ranks_of_nations[1]))
cursor.close()




