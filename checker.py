from bs4 import BeautifulSoup
import urllib
from urllib.request import urlopen
import sqlite3
import json
import operator

def createDatabaseConnect(dbName):
	con = sqlite3.connect(dbName)
	cur = con.cursor()
	return cur , con
# create table and store the details
dbName = "OlympicsData.db"
cursor,con = createDatabaseConnect(dbName)


query = "SELECT * from SummerOlympics"
result = cursor.execute(query)
flag=0
for row in result:
    if(row[-1]=='0'):
        flag=1
if(flag==0):
    print("All the rows are populated!")
    print('choosen years:')
    query = "SELECT DISTINCT year from SummerOlympics"
    result = cursor.execute(query)
    result=result.fetchall()
    for i in result:
        print(i[0],end=' ')
    print()
    query = "SELECT Athletes from SummerOlympics"
    result = cursor.execute(query)
    result=result.fetchall()
    count=0
    sum=0
    for i in result:
        sum+=int(i[0])
        count+=1
    print("Average number of athelete: ",sum//count)
    query = "SELECT Rank_1_nation,Rank_2_nation,Rank_3_nation from SummerOlympics"
    result = cursor.execute(query)
    result=result.fetchall()
    common={}
    for i in result:
        for j in range(len(i)):
            if(i[j] not in common):
                common[i[j]]=1
            else:
                common[i[j]]+=1
    print("most common country: ",max(common.items(), key = operator.itemgetter(1))[0]
)
else:
    print("Still some rows need to populate")

