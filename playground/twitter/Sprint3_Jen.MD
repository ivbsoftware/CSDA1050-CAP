SPRINT 3 PLAN - TWITTER TWEETS
==============================

###### Jennifer Johnson

## What has been done?
1. Twitter Stream - data collected from March 18, 2019 to April 10, 2019 (partial) with some intermittent gaps when the process failed.  "twitter_stream_post.py"
2. Clean/Parse data - combined all stream files into 2 files tweets and users (users file is shared with Ariana). "tweet_data.py"
3. EDA - minimum work done on EDA, spent most time with additional cleaning and formatting of the data. "twitter_analysis.ipynb"

## What planned to do Sprint 3
1. Some additional cleaning
  - remove hashtags from tweet (already in a separate column and don't want them to interfere with other text)
  - fix language detection and translation (after looking at it again I found it wasn't working as I thought... exploring other libraries... nltk.misc (babelfish) and googletrans
2. Additional Analysis
  - Topic Analysis - similar to Igor's analysis
  - Geo/Maps Analysis - similar to Michael's analysis
  - Topic and Maps together ... maybe could be compared to Igor's GDELT data
  - User Language vs Tweet Language (depends on how cleaning goes in 1)
  - Mentions in Tweets to users ?? 
3. Search internet for other twitter analysis already done and see if I can incorporate it into mine 
4. Time permitting 
  - clean up code to put all cleaning together
   - review columns in stream files to check for additional fields with usable information
   - merge users and tweets into 1 file
   - get Ariana's twitter data and merge with mine to check if it resolves some of the gaps, or if we get different tweets during the same period.
