# Web Scraping with Python

Here we will learn How to collect data from different ways, like through API, through unstructured data like website and and to store them in database
in structured manner so that for futher it is better to analyse it.
We'll use the basic architecture of a scraper and utilize various Python libraries for these tasks.

# Setting Up Your Environment

requests and urllib3: For sending GET requests and receiving data.
json: For processing structured data.
beautifulsoup4 (bs4): For parsing and processing unstructured data.
sqlite3: For storing data in a local SQLite database.
random: For random sampling.
Command to install the python library: pip3 install <libraryname>

## 1: Collect and Store Structured JSON Data
Here We collect weather data from the OpenWeatherMap API and store it in SQLite database.

Make API calls to the OpenWeatherMap API using your API key.
Extract relevant information from the API response, such as city name, temperature, weather description, humidity, and wind speed.
Create a SQLite database named Weather.db and a table named city_weather to store the extracted data.
Insert the extracted data into the city_weather table.
Test your system with three to five different cities of your choice, included in a test function in Api_data.py

## 2: Collecting, Storing, and Processing Unstructured Data (i.e webpages)

Here we were collecting information about Summer Olympics from its Wikipedia page, processing the data, and storing it in a SQLite database.

Collect Wikipedia Page: Request the main page of Summer Olympics Wikipedia from link.

SQLite Database: Create a SQLite database named OlympicsData.db and a table named SummerOlympics with the following columns:

Name (e.g. “2012 Summer Olympics”, in title of respective Wikipedia pages)
WikipediaURL
Year (the year when it's conducted)
HostCity (the city where it's hosted)
ParticipatingNations (List of the participating nations)
Athletes (number of athletes)
Sports (list of sports)
Rank_1_nation
Rank_2_nation
Rank_3_nation
Parse HTML and Extract URLs: Parse the HTML page and extract the Summer Olympics wiki page URLs for random 2 Olympics from the last 50 years (i.e., from 1968 to 2020). You can try parsing the “List of Summer Olympic Games” table to get the URLs and use random.sample for random sampling.

Extract Data and Insert into Database: For each of the pages of your two selected Summer Olympics, extract the data using BeautifulSoup mentioned in step 2 and insert it into the database.

Data Analysis: Using the database, print answers to the following questions:

What are the years you chose?
What is the average number of countries participating in the two Olympics?
Print the overlap (i.e., common nations) within <Rank_1_nation, Rank_2_nation, and Rank_3_nation> for your chosen two years.
Done in unstructured data.py

## 3: Using Multiple Processes to enhance the speed

In this task, we will enhance the data collection process by utilizing multiple processes for speed up. The goal is to collect information about different Summer Olympics from Wikipedia pages and store the data in a SQLite database.

### Task Description

Handler Function: Write a handler function that performs the following tasks:
Collect the main page of Summer Olympics Wikipedia.
Create a SQLite database named 'OlympicsData.db' and a table named 'SummerOlympics' with the specified columns.
Parse the HTML to extract the individual Summer Olympics wiki page URLs for ten Olympics from the last 50 years, i.e., from 1968 to 2020.
Insert the Wikipedia URLs into the database and set the 'DONE_OR_NOT_DONE' flag as 0 for all rows.
Done in muliple processes.py

Spawn Processes: The handler code will spawn three processes using the os.system call to run the scraper script concurrently.
Example of this call import os os.system(“python3 scraper.py&”) This will run “python3 scraper.py” in a separate process.

Scraper Script (scraper.py): This script will perform the following tasks:

Check the database for rows where the 'DONE_OR_NOT_DONE' flag is 0.
Pick a row where 'DONE_OR_NOT_DONE' is 0. If no such row exists, the script will exit.
Set the 'DONE_OR_NOT_DONE' flag to 1 for the chosen row.
Fetch the Wikipedia page using the URL in the 'WikipediaURL' column.
Parse the page using BeautifulSoup and populate the corresponding columns in the database.
Checker Script (checker.py): This script will check the database and:

Report if all the database rows are populated (i.e., 'DONE_OR_NOT_DONE' is set to 0 and no process is working).
If all database rows are populated, print answers to the specified questions.
Implementation

Here's a high-level overview of the implementation:

Write the handler function to perform the initial setup, database creation, and URL extraction.
Implement the scraper script to fetch and parse Wikipedia pages concurrently using multiple processes.
Develop the checker script to monitor the database and report completion status.
Execute the handler function to initiate the data collection process.
Run the scraper script in parallel processes to fetch and process Wikipedia pages.
Use the checker script to ensure that all data has been collected and perform any final analysis or reporting.
