#Problem: To collect the weather data using API
#and store it in a local SQLite database
# so basically data is structured here so we can process it using the json library in python
import requests
import sqlite3
import json
from bs4 import BeautifulSoup

def getData(url):
    response = requests.get(url)
    #convert to text string and return 
    return response.text

def convertJson(data):
    return json.loads(data)

def createDatabaseConnect(dbName):
	con = sqlite3.connect(dbName)
	cur = con.cursor()
	return cur , con
url = 'http://api.openweathermap.org/data/2.5/weather?lat=44.34&lon=10.99&appid=8d8b84a428daf68c5246370daafbc224'
weatherDetails = getData(url)
jsonWeather = convertJson(weatherDetails)
dbName = "weather.db"
cursor,con = createDatabaseConnect(dbName)

## Now you can create Table and insert/select records from there
## Lets create a Table "example" with three columns a, b and c to insert the structured data 
## we fecthed earlier

query = "CREATE TABLE IF NOT EXISTS city_weather(city_name, Temperature, Description,Humidity,WindSpeed)"
cursor.execute(query)

#print(jsonWeather)
if(jsonWeather['cod']==200):
    main=jsonWeather['main']
    wind=jsonWeather['wind']
    weather=jsonWeather['weather']
    query = "INSERT INTO city_weather VALUES ('%s', '%s', '%s', '%s', '%s')"%(jsonWeather["name"], main["temp"], weather[0]["description"], main["humidity"], wind["speed"])
    cursor.execute(query)
    con.commit()


## Lets see what is in the table
query = "SELECT * from city_weather"
result = cursor.execute(query)
for row in result:
	print(row)
cursor.close()
