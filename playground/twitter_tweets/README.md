# CSDA1050-CAP: Twitter Analysis (Tweets)

This purpose of this project is to Stream, Clean, and Analyze Twitter data for Toronto.  The initial plan was to align and find relationships between Twitter data, GDELT articles in the GTA, and real estate information.  Due to the limitations in some of the web scrapped data from other web sites and the limited GEO tagged Twitter data, the analysis of Twitter data was to see if there was anything interesting in the Twitter data using GEO/maps, Sentiment Analysis, Topic Analysis, and general text analysis.

## Configuration Instructions

This section outlines the libraries used, installation instructions, and setup for Streaming, Parsing, and Analyzing the data from Twitter.

### Libraries

 * tweepy
 * time
 * sys
 * os
 * pandas
 * json
 * emoji
 * datetime
 * real
 * vaderSentiment.vaderSentiment
 * spacy
 * nltk
 * string
 * ast
 * numpy
 * seaborn
 * missingno
 * wordcloud
 * matplotlib.pyplot
 * pytz
 * geopandas
 * shapely.geometry
 * shapefile
 * spacy.lang.en
 * nltk.corpus
 * nltk.stem.wordnet
 * translate
 * gensim
 * pickle
 * pyLDAvis.gensim

### Installing Libraries

To install libraries for Python, when using Idle (standalone Python)
```
pip install <library>
```

To install libraries using Jupyter
```
import sys
!{sys.executable} -m pip install <library>
```

### Twitter Development Account for Streaming
Go to https://developer.twitter.com/content/developer-twitter/en.html and create a Twitter Developer account
Create an App, and go to Keys and tokens


## List of Files
 * twitter_stream_post.py - Stream Twitter data to a file
 * twitter_clean_data_v2.py - Flatten, structure and store Tweets and Users to csv files
 * Tweet_Analysis_v1.ipynb - Jupyter exploratory data analysis - no Filters
 * Tweet_Analysis_v2.ipynb - Jupyter exploratory data analysis - Toronto Only 
 * Tweet_Analysis_v3.ipynb - Jupyter exploratory data analysis - GEO tagged Only
 * Tweet_Sentiment_Analysis_v1.ipynb - Jupyter sentiment exploratory data analysis - Toronto Only
 * Tweet_Sentiment_Analysis_v2.ipynb - Jupyter sentiment analysis, data cleanse v1 - Toronto Only
 * Tweet_Sentiment_Analysis_v3.ipynb - Jupyter sentiment analysis, data cleanse v2 - Toronto Only
 * Twitter_Maps_v2.ipynb - Jupyter geopanda Toronto Maps Analysis
 * Twitter_Topic_Modeling_v2.ipynb - Jupyter Topic Modeling, data cleanse v2
 * Twitter_Topic_Modeling_v3.ipynb - Jupyter Topic Modeling, data cleanse v3 

## Operating Instructions

### How to stream data
To run streaming code, open a command prompt and run code using:
```
python twitter_stream_post.py > file_to_store_tweets.txt
```
Code will run until connection is lost or stopped using CTRL+C

### Cleaning, Parsing, and Structuring Tweets
To run cleaning code, add streaming files to a folder called "stream_files" in the folder where the code is running from.  The code can be run from the command line using:
```
python twitter_clean_data_v2.py
```

### Analysis
To run the analysis, open Jupyter Notebook.  Run step by step or run all lines. 


## Known Bugs and Limitations
 * Limitation with streaming data, there is a limitation, if the program crashes or there is a loss of connection streaming is stopped and will need to be started again manually.  
 * Performance of cleaning and parsing is very slow for large files
 