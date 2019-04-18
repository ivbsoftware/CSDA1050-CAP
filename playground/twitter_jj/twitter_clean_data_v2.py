# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 19:28:58 2019

@author: Jennifer
"""
# Libraries
import sys
import os
import pandas as pd
import json
import emoji
from datetime import datetime
#from slugify import slugify
import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


##-------------------------------------------------------------------
## Set Global Variables (dataframes)
##-------------------------------------------------------------------
def setGlobalVariables():
    global user_df
    global tweet_df

    ## ------------------------------------------------------
    ## User DataFrame
    user = {'id', 'user_name', 'screen_name', 'location', 'description',
            'protected', 'verified', 'followers_count', 'friends_count',
            'listed_count', 'favourites_count', 'statuses_count',
            'created_date', 'geo_enabled', 'language', 'contributors_enabled'
            }
          
    user_df = pd.DataFrame(columns=user)
    ## ------------------------------------------------------

    ## ------------------------------------------------------
    ## Tweets DataFrame
    tweet = {'id', 'tweet_date', 'tweet_text', 'latitude', 'longitude',
             'source', 'hashtags', 'mentions', 'reply_to_user', 'reply_to_status',
             'quote_status', 'language', 'place_type', 'place_name',
             'place_country', 'place_bbtype', 'place_bbcoordinates', 'sensitive',
             'quoted_text', 'quoted_id', 'user_id', 'user_name',
             'emojis', 'sentiment', 
            }
          
    tweet_df = pd.DataFrame(columns=tweet)
    ## ------------------------------------------------------
    
    return


##-------------------------------------------------------------------
## Process Twitter Stream Files
##-------------------------------------------------------------------
def processFiles(path, user_df, tweet_df):
    directory = os.fsencode(path)
    print(directory)   
    
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.startswith('toronto_twitter'):
            file_path = os.path.join(path, filename)
            print(file_path)
            
            # open file
            twitter_file = open(file_path, mode='r', encoding='utf-8')

            for line in twitter_file:
                try:
                    tweet = json.loads(line)

                    ## USER DATA
                    ## ------------------------------------------------------
                    user_record = cleanUser(tweet)                        
                    user_id = user_record.iloc[0]['id']
                    if not (user_df['id'] == user_id).any():
                        # insert record in dataframe             
                        user_df = user_df.append(user_record)

                    ## TWEET DATA
                    ## ------------------------------------------------------
                    tweet_record = cleanTweet(tweet)
                    tweet_id = tweet_record.iloc[0]['id']
                    if not (tweet_df['id'] == tweet_id).any():
                        # insert record in dataframe
                        tweet_df = tweet_df.append(tweet_record)
                except:
                    # if error, continue to next record
                    continue

            print('%s Users, %s Tweets' %(len(user_df.index), len(tweet_df.index)))

            # export to files as we go.
            # Make sure files are not opened while still running to reduce errors
            user_df.to_csv(r'twitter_users_new.csv', index=False)
            tweet_df.to_csv(r'twitter_tweets_new.csv', index=False)
        else:
            continue    

    return
    
##-------------------------------------------------------------------
def cleanTweet(tweet):
    tweet_id = tweet['id']
    tweet_date = tweet['timestamp_ms']
    
    if 'extended_tweet' in tweet:
        tweet_text = cleanEmoji(EncodeDecode(tweet['extended_tweet']['full_text']))
        tweet_emoji = findEmoji(tweet['extended_tweet']['full_text'])
    else:
        tweet_text = cleanEmoji(EncodeDecode(tweet['text']))
        tweet_emoji = findEmoji(tweet['text'])

    sentiment = getSentiment(tweet_text)

    # split coordinates into latitude and longitude
    if tweet['coordinates'] is not None:
        lat_long = tweet['coordinates']['coordinates']
        tweet_longitude = lat_long[0]
        tweet_latitude = lat_long[1]
    else:
        tweet_longitude = None
        tweet_latitude = None
    
    tweet_source = re.sub(re.compile('<.*?>'), '', tweet['source'])           
    tweet_hashtags = None if tweet['entities']['hashtags'] == [] else cleanList(tweet['entities']['hashtags'], 'text')
    tweet_mentions = None if tweet['entities']['user_mentions'] == [] else cleanList(tweet['entities']['user_mentions'], 'screen_name')
    tweet_reply_to_user = tweet['in_reply_to_screen_name'] if 'in_reply_to_screen_name' in tweet else None
    tweet_reply_to_status = tweet['in_reply_to_status_id'] if 'in_reply_to_status_id' in tweet else None

    if 'quoted_status' in tweet:
        tweet_quote_status = tweet['is_quote_status']
        tweet_quoted_text = cleanEmoji(EncodeDecode(tweet['quoted_status']['text']))
        tweet_quoted_id = tweet['quoted_status_id']
    else:
        tweet_quote_status = 'false'
        tweet_quoted_text = None
        tweet_quoted_id = None
        
    tweet_language = tweet['lang']
    tweet_place_type = tweet['place']['place_type']
    
    tweet_place_name = tweet['place']['full_name']  
    tweet_place_country = tweet['place']['country']
    tweet_place_bbtype = tweet['place']['bounding_box']['type']
    tweet_place_bbcoordinates = tweet['place']['bounding_box']['coordinates']
    tweet_sensitive = tweet['possibly_sensitive'] if 'possibly_sensitive' in tweet else False

    user_id = tweet['user']['id']    
    user_screen_name = tweet['user']['screen_name']

    
    tweet_record = [
        { 'id':tweet_id,
          'tweet_date':tweet_date,
          'tweet_text':tweet_text,
          'latitude':tweet_latitude,
          'longitude':tweet_longitude,
          'source':tweet_source,
          'hashtags':tweet_hashtags,
          'mentions':tweet_mentions,
          'reply_to_user':tweet_reply_to_user,
          'reply_to_status':tweet_reply_to_status,
          'quote_status':tweet_quote_status,
          'language':tweet_language,
          'place_type':tweet_place_type,
          'place_name':tweet_place_name,
          'place_country':tweet_place_country,
          'place_bbtype':tweet_place_bbtype,
          'place_bbcoordinates':tweet_place_bbcoordinates,
          'sensitive':tweet_sensitive,
          'quoted_text':tweet_quoted_text,
          'quoted_id':tweet_quoted_id,
          'user_id':user_id,
          'user_name':user_screen_name,
          'emojis':tweet_emoji,
          'sentiment':sentiment
          }
        ]
    
    source_df = pd.DataFrame(tweet_record)

    # convert date to proper datetime datatype
    source_df['tweet_date'] = pd.to_datetime(source_df['tweet_date'], unit='ms')
        
    return source_df


##-------------------------------------------------------------------
def cleanUser(tweet):
    user_id = tweet['user']['id']
    user_name = None if tweet['user']['name'] is None else cleanEmoji(EncodeDecode(tweet['user']['name']))
    user_screen_name = tweet['user']['screen_name']
    user_location = None if tweet['user']['location'] is None else EncodeDecode(tweet['user']['location'])        
    user_description = None if tweet['user']['description'] is None else cleanEmoji(EncodeDecode(tweet['user']['description']))
    user_protected = None if tweet['user']['protected'] is None else tweet['user']['protected']
    user_verified = None if tweet['user']['verified'] is None else tweet['user']['verified']
    user_followers_count = None if tweet['user']['followers_count'] is None else tweet['user']['followers_count']
    user_friends_count = None if tweet['user']['friends_count'] is None else tweet['user']['friends_count']
    user_listed_count = None if tweet['user']['listed_count'] is None else tweet['user']['listed_count']
    user_favourites_count = None if tweet['user']['favourites_count'] is None else tweet['user']['favourites_count']
    user_statuses_count = None if tweet['user']['statuses_count'] is None else tweet['user']['statuses_count']
    user_created_date = None if tweet['user']['created_at'] is None else tweet['user']['created_at']
    user_geo_enabled = None if tweet['user']['geo_enabled'] is None else tweet['user']['geo_enabled']
    user_language = None if tweet['user']['lang'] is None else tweet['user']['lang']
    user_contributors_enabled = tweet['user']['contributors_enabled'] if 'contributors_enabled' in tweet else 'false' 


    user_record = [
        { 'id':user_id
          , 'user_name':user_name
          , 'screen_name':user_screen_name
          , 'location':user_location
          , 'description':user_description
          , 'protected':user_protected
          , 'verified':user_verified
          , 'followers_count':user_followers_count
          , 'friends_count':user_friends_count
          , 'listed_count':user_listed_count
          , 'favourites_count':user_favourites_count
          , 'statuses_count':user_statuses_count
          , 'created_date':user_created_date
          , 'geo_enabled':user_geo_enabled
          , 'language':user_language
          , 'contributors_enabled':user_contributors_enabled
          }
        ]
    source_df = pd.DataFrame(user_record)
    
    return source_df
    

##-------------------------------------------------------------------
def getSentiment(text):
    # look through text to find emojis
    value = {}
    
    analyser = SentimentIntensityAnalyzer()

    value = analyser.polarity_scores(text)
    #print(value)
    
    return value


##-------------------------------------------------------------------
def findEmoji(text):
    # look through text to find emojis
    value = []
    
    #data = re.findall(r"\x",text)
    #print(data)
    for word in text:
        if any(char in emoji.UNICODE_EMOJI for char in word):
            word = cleanEmoji(word)
            value.append(word)
    
    return value


##-------------------------------------------------------------------
def cleanList(listDict, column):
    # cycle through list of dictionaries to get column values
    value = []
    
    if not(listDict == []):
        for item in listDict:
            value.append(item[column])
        
    return value


##-------------------------------------------------------------------
def EncodeDecode(value):
    # fixes unicode characters to make more readable
    value = value.encode('utf-8').decode('utf-8')
    return value


##-------------------------------------------------------------------
def cleanEmoji(value):
    # converts emojis to text
    value = emoji.demojize(value)
    return value
    

##-------------------------------------------------------------------
## Main 
##-------------------------------------------------------------------
if __name__ == '__main__':
    
    directory = os.path.dirname(os.path.abspath(__file__))
    path = '%s\stream_files' %(directory)

    setGlobalVariables()
    print(user_df)
    print('Processing Files...')
    processFiles(path, user_df, tweet_df)
