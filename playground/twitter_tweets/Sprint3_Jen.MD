SPRINT 3 PLAN - TWITTER TWEETS
==============================

###### Jennifer Johnson

## What has been done?
1. Twitter Stream 
 - "twitter_stream_post.py"
 - data collected from March 18, 2019 to April 10, 2019 (partial) 
 - some intermittent gaps when the process failed, better if there was ability to restart if failed
2. Clean/Parse data 
 - "tweet_data.py"
 - combined all stream files into 2 files tweets and users (users file is shared with Ariana). 
 - check for duplicate users and tweets to prevent duplicates in clean file
3. EDA 
 - "twitter_analysis.ipynb"
 - load data, record count, clean date/time, check datatypes
 - view tweets by day using line graph
 - view tweets by hour using line graph
 - view tweets by day of week using line graph
 - get count of tweets by user, show top 5 users
 - clean tweets and remove stopwords
 - create word cloud of tweets
 - clean hashtags 
 - create word cloud of hashtags

## What planned to do Sprint 3
1. Some additional cleaning/fixes
  - remove hashtags from tweet (already in a separate column and don't want them to interfere with other text)
  - fix language detection and translation (after looking at it again I found it wasn't working as I thought... exploring other libraries... nltk.misc (babelfish) and googletrans
  - switch hour of day and day of week graphs to bar graphs
2. Additional Analysis
  - Topic Analysis - similar to Igor's analysis
  - Geo/Maps Analysis - similar to Michael's analysis
  - Topic and Maps together ... maybe could be compared to Igor's GDELT data
  - User Language vs Tweet Language (depends on how cleaning goes in 1)
  - Mentions in Tweets to users ?? 
3. Search internet for other twitter analysis already done and see if I can incorporate it into mine 
4. Other  
  - clean up code to put all cleaning together
   - review columns in stream files to check for additional fields with usable information
   - merge users and tweets into 1 file
   - get Ariana's twitter data and merge with mine to check if it resolves some of the gaps, or if we get different tweets during the same period.
