#Kijiji_Rental 

1.  ETL and Data Gathering:

    ---scrapyjiji.py   is the original scraper, downloaded from https://github.com/CRutkowski/Kijiji-Scraper.
    This scraper developed on library Beatifulsoup 4, it captured all AD url and general AD information from the Kijij url you pass to it.     It does not capture all detailed data from individual Kiji AD webpages;
    
    ---main.py   In this script, I call the scrapyjiji.py to download all AD urls and store them into txt file. Kijiji Rent does not has       Categories, so I need to search the ADs by clicking on the tags on the search page.  Such as 'One Bed room'. My code will create a txt     file for each AD tag to store all AD urls.
    
    ---Kijiji-Scraper_s.py  I modified the original scraper, rewrote the "ParseAd" function so it can scrape data from single AD web           pages. It stores all data into a .txt file in dictionary format.
	Due to Kijiji's anto-span     protection, Kijiji b
	##-> Extraction from API
	
	##-> Transforming/Loading to DB
	
	##-> EDA Notebook
	
