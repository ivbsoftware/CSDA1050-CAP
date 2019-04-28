***************************
In this class, by working on actual Kijiji data, I experienced the 'unformatted data' and had a lot of practicing on Pycharm.  

  I) Previously, I have always been working with ERP (structured) data. They are welly structured and easy to clean and manage.  But when I was working with unstructured data, I realized it's really complicated to clean the data accurately and completely.  
  
  II) While working on the project, I got chance to work on popular Python libraries and Pycharm IDE.  Pycharm is an excellent Python IDE, has very strong debugging features and it really helped me to understand the structures of dataframs, serious, array, dictionary and teach me a way to access right data by using parameters.  I start to like this IDE and will practice on my own projects.

  III) Google Cloud:  I have tried Oracle Cloud, AWS but this is my first time of trying Google Cloud.  Google cloud has very flexible trial policies, excellent hardware/VM environment and provide almost everything you need for managing business and analysis project.  Very interesting platform and I will do more research.
  
***************************
#Kijiji_Rental
##-> Extraction from API

requests      BeautifulSoup      datetime     time

Sys              os                         re                geocode

Csv              pandas                 psycopg2    numpy 

matplotlib.pyplot      geopandas      missingno

psycopg2     scipy

##->  ETL and Data Gathering:

---scrapyjiji.py is the original scraper, downloaded from https://github.com/CRutkowski/Kijiji-Scraper. This scraper developed on library Beatifulsoup 4, it captured all AD url and general AD information from the Kijij url you pass to it. It does not capture all detailed data from individual Kiji AD webpages;

---main.py In this script, I call the scrapyjiji.py to download all AD urls and store them into txt file. Kijiji Rent does not has Categories, so I need to search the ADs by clicking on the tags on the search page. Such as 'One Bed room'. My code will create a txt file for each AD tag to store all AD urls.

---Kijiji-Scraper_s.py I modified the original scraper, rewrote the "ParseAd" function so it can scrape data from single AD web pages. It stores all data into a .txt file in dictionary format. It gather detailed data, such as AD postdate, address and number of bathrooms.

---Main_scr_all_pages.py.  This script calls Kijiji-Scraper_s.py to scrape all detailed AD data from the AD urls we gathered from main.py.  Due to Kijiji's span protection, Kijiji block my IP address when my requests reach 2000.  So I break down the total urls into smaller group, each group has about 2000 urls.  It store data in a few txt files.

##-> Transforming/Loading to DB

--- Convert_CSV2.py  Read all the txt file that created from Main_scr_all_pages.py, append them into one dataframe file, drop duplicated on AD_ID, then store into a csv file.

--- Insert_Table.py  Insert all data into a Postgres table, hosted on Google Cloud.

##-> EDA Notebook: Project.ipynb  data cleaning and data analysis


******* For details, please review:https://github.com/ivbsoftware/CSDA1050-CAP/blob/master/playground/Kijiji/GTA%20Affordable%20Housing%20-%20Kijiji%20Data%20Analysis.docx
