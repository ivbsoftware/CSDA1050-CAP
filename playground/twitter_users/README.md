Twitter Sentiment Analysis
This folder contains the code used to perform a Twitter text and sentiment analysis

Step 1 - Retrieve Tweets using Twitter API

Create a new application on apps.twitter.com and take note of the API and access tokens.
First you will need define your keysand import the below packages: 

import tweepy as tw
import pandas as pd

consumer_key= 'yourkeyhere'
consumer_secret= 'yourkeyhere'
access_token= 'yourkeyhere'
access_token_secret= 'yourkeyhere'

auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)

Next, run streaming code using: python twitter_stream_post.py > file_to_store_tweets.txt


Step 2 - Identify Hashtags 
Before cleaning out special characters from tweets, identify hashtags and create a new column for them. Clean and complete analysis on hashtags. 


Step 3 - Clean, tokenize, and stem tweets 
Remove twitter handels, sepecial characters, punctuation, urls, and short words. Then, tokenize and stem tweets. 
Doing this will make tweet data easier to analyse. 

Step 4 - Analyse 
Assign sentiment scores to cleaned tweets, create word clouds, and identify most frequently used terms 
