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
# create table and store the details
dbName = "OlympicsData.db"
cursor,con = createDatabaseConnect(dbName)
query = "SELECT id,done,WikipediaURL from SummerOlympics where done='0'"
result = cursor.execute(query)
results=cursor.fetchall()
for row in results:
    if(row[1]=='0'):
    	html = urlopen(row[2])
    	list_countries=[]
    	list_sports=[]
    	specificGame = html.read()
    	soup = BeautifulSoup(specificGame, 'html.parser')
    	details=soup.find_all('td',attrs={'class':'infobox-data'})
    	name=soup.find('span',attrs={'class':'mw-page-title-main'}).text
    	year=name.split()[0]
    	url1=row[2]
    	hostCity=details[0].text.split(',')[0]
    	nation=soup.find('th',string='Nations').find_next('td').text.split()[0].strip()
    	no_of_athelete=soup.find('th',string='Athletes').find_next('td').text.strip().split()[0].split('[')[0].replace(',','')
    	tables = soup.find('table',attrs={'class':'plainrowheaders'}).find('tbody').find_all('tr')
    	rank1=tables[1].find('th').a.text
    	rank2=tables[2].find('th').a.text
    	rank3=tables[3].find('th').a.text
    	listofnations = soup.find('span',string='Participating National Olympic Committees').find_next('table').find_all('li')
    	for j in listofnations:
    	    if(j.a.text!=""):
    	        query="INSERT INTO Countries VALUES ('%d','%s')"%(row[0],j.a.text.strip())
    	        cursor.execute(query)
    	cursor.execute("UPDATE SummerOlympics SET done=? where id=?",('1',row[0]))
    	cursor.execute("UPDATE SummerOlympics SET Name=?, WikipediaURL=?, Year=?, HostCity=?, Athletes=?, Rank_1_nation=?, Rank_2_nation=?, Rank_3_nation=?, nation=? where id=?" ,(name,url1,year,hostCity,no_of_athelete,rank1,rank2,rank3,nation,row[0]))
    	con.commit()
else:
    print('issue')
    cursor.close()
    exit(0)

