# CSDA1050-CAP

TREB 

Treb Rental Repo

Request method: GET

url= "https://listings.trebhome.com/listings?%24loc=Toronto&%24zoom=0&%24latitude=35.422943522054865&%24longitude=0&%24orderby=price&saleOrRent=RENT&latitude=%3E%3D-89.91227567527925&latitude=%3C%3D89.9766532819623&longitude=%3E%3D-180&longitude=%3C%3D180&%24gid=treb&class=FREE&class=CONDO&availability=A&_min_price=%24300&price=%3E%3D300&price=%3C%3D50000&area=Toronto&%24take=3164"

Request filter: Loc: Toronto, min_price: $300 ( exclude locker and parking spot lease priced below $300), max_price:$50,000
                posted date: March 20- March 24,2019

Web Scraping Method: Use BeautifulSoup and Requests with Python ( see Request py code file )

Request Header: ID Address Bedrooms Bathrooms Type Price

The final output dataset is written as " rental1.csv".

ETL " rental1.csv" into R with coding in file " Rental_Freq_Summary_Modelling", clean, remove duplicates and missing values, 
change datatype.

Analsis including :

1) Statistics about Price, Bedrooms , Bathrooms ( min, max, mean , median, Q1,Q3)
2) Look into counts(frequency) by Type and visualization
3) Look into Price distribution related to Type , Bedrooms, Bathrooms
4) Find Top 10 Type by the Number of Properties
5)  Find Top 10 Type by the Average Price of Properties

6) Summarize the Price with Type, Bedrooms, Bathrooms and Look at Price Trend 
     (see Summary_Type_Beds_Bath.csv)
     Look at one specific example: # Look the price trend in Type  “Detached 2-storey”

7) Summarize the Price with Bedrooms, Bathrooms and Look at Price Trend
(See Summary_Beds_Baths.csv)

8) Summarize the Price with Bedrooms and Look at Price Trend ( High level summary)
(See Summary_Beds.csv)

Project Modelling Analysis including:

1) train dataset 80% , test dataset 20%
2) decision tree model 
3) Random Forest model with 500 trees
4) Evaluate models: compare decision tree vs Random Forest model ( rmse or mae )
5) Regression Model
Model 1: Look at Price with Bedrooms and Bathrooms
Model 2: Look at log(Price) with Bedrooms and Bathrooms  (To overcome heteroskedasiticity with buiding log(Price)).
6) Evaluate models: compare Model1 vs Model 2, look at Adjusted R squared and p-value. 
                    compare rmse or mae 
7) write the formula for Regression Model


Discuss project challenge.


	
	
