# Craigslist_Rental
This folder contains the code used to perform the analysis, as well as the resulting report.

## Steps to Reproduce

### Step 1 - ETL
Run the Craigslist ETL.py script. 

This script uses the [Craigslist Library](https://pypi.org/project/python-craigslist/) to download, clean and store listings for the greater toronto area. 

The script converts the data recovered to the appropriate data type, separates Geolocation to Lat/Long, separates area (which includes unit on the end) into an integer for area and area unit.
The script then stores the file in a MS SQL database, connected through a pre established ODBC DSN connection. The DSN connection is established using the ODBC Datasource Administrator tool on Windows. There are no checks for duplicates, this is done in the EDA.

### Step 2 - EDA
Run the Craigslist Rental EDA.ipynb script. 

The EDA in this script checks for duplicates and reposts using the post ID. Once identified, these are removed from the dataset. Most of the missing data found are from a first trial data extraction where I opted to drop certian columns (URL, Index, has_image). These missing items have little impact on the rest of the analysis. The notable columns (area, price, lat/lon) are mostly complete. The bedroom data though has a good number of missing values. 

The script also extracts the listings' body and title, then tokenizes the text. The result of this is then used to extract whether the listings are basement or studio apartments. 

This script then stores the cleaned dataset in a csv file to then be easily re-imported and used again. 

Step 3 - Detailed Analysis
Run the Craigslist Detailed Analysis.ipynb script

This script performs a geographical analysis of the listings using a map of toronto from the [Toronto Open Data Portal](https://www.toronto.ca/city-government/data-research-maps/open-data/open-data-catalogue/#a45bd45a-ede8-730e-1abc-93105b2c439f). 

The tokenized text is investigated for different words used for the different cost quartiles of rentals. 

The listing data is then compared to census data extracted from [SimplyAnalytics](https://simplyanalytics.com/). 

Lastly, models are build using all of the relevant information to establish feature importance. These models are rudimentary and do not have any parameter tuning.