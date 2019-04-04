# Libraries
import pandas as pd
import json
import emoji
from datetime import datetime
from slugify import slugify
import re


#----------------------------------------------------------------------   
##
### Define columns for User DataFrame
##user = {'id', 'user_name', 'screen_name', 'verified', 'followers_count',
##        'friends_count', 'favourites_count'}
##
##user_df = pd.DataFrame(columns=user)
##
### Define columns for Tweet DataFrame
##tweet = {'id', 'tweet_date', 'tweet_text', 'latitude', 'longitude',
##         'reply_count', 'retweet_count', 'source', 'hashtags',
##         'mentions', 'favourites_count', 'user_id'}
##
##tweet_df = pd.DataFrame(columns=tweet)
##
#-----------------------------------------------------------------------

# Load existing data into dataframe
try:
    user_df = pd.read_csv("twitter_users.csv")
    # check that all columns are present
    user_col_list = ['id', 'user_name', 'screen_name', 'verified', 'followers_count',
                 'friends_count', 'favourites_count', 'description']

    user_df = user_df.loc[:, user_col_list]
except FileNotFoundError:
    ### Define columns for User DataFrame
    user = {'id', 'user_name', 'screen_name', 'verified', 'followers_count',
            'friends_count', 'favourites_count', 'description'}

    user_df = pd.DataFrame(columns=user)
    
tweet_df = pd.read_csv("twitter_tweets.csv")


# Improvements... cycle through list of files beginning with 'toronto_twitter_data'
# Total: 184019 tweets 25432 users

#tweets_data_path = 'toronto_twitter_data_20190327.txt' ## LOADED -- tweets 5240 -- users 2169 --
#tweets_data_path = 'toronto_twitter_data_20190317.txt' ## LOADED -- tweets +4833 -- users +1495 --
#tweets_data_path = 'toronto_twitter_data_20190318a.txt' ## LOADED -- tweets +4139 -- users +951 --
#tweets_data_path = 'toronto_twitter_data_20190318b.txt' ## LOADED -- tweets +181 -- users +60 --
#tweets_data_path = 'toronto_twitter_data_20190318c.txt' ## LOADED -- tweets +59158 -- users +8554 --
#tweets_data_path = 'toronto_twitter_data_20190322.txt' ## LOADED -- tweets +90046 -- users +7478 --
#tweets_data_path = 'toronto_twitter_data_20190330.txt' ## LOADED -- tweets +20424 -- users +1854 --
tweets_data_path = 'toronto_twitter_data_20190331.txt'
#tweets_data_path = 'toronto_twitter_data_20190402.txt'

# open file
tweets_file = open(tweets_data_path, mode="r", encoding='utf-8')
#with io.open(tweets_data_path, 'r', encoding='utf-8') as file:
#    tweets_file = file.read()

# read the data into an array
for line in tweets_file:
    try:

        tweet = json.loads(line)

        # FLATTEN DATA

        #---------------------------------------------------------------
        # USER DATA
        #---------------------------------------------------------------
        user_id = tweet['user']['id']

        # Cleanup user name, and convert emoji to text
        x = tweet['user']['name']
        x = x.encode('utf-8').decode('utf-8')
        x = emoji.demojize(x)
        #x = slugify(x)

        # Cleanup user description, and convert emoji to text
        d = tweet['user']['description']
        d = d.encode('utf-8').decode('utf-8')
        d = emoji.demojize(d)
        
        user_record = [
            { 'id':tweet['user']['id'],
              'user_name':x, 
              'screen_name':tweet['user']['screen_name'],
              'description':d,
              'verified':tweet['user']['verified'],
              'followers_count':tweet['user']['followers_count'],
              'friends_count':tweet['user']['friends_count'],
              'favourites_count':tweet['user']['favourites_count']
              }
            ]
        source_df = pd.DataFrame(user_record)

        # check if user exists in dataframe
        if not (user_df['id'] == user_id).any():            
            # insert record in dataframe
            user_df = user_df.append(source_df)
##        else:
##            # update record in dataframe
##            user_df.set_index('id')
##            source_df.set_index('id')
##            user_df.update(source_df)
##
##            user_df.reset_index(drop=False)
##            source_df.reset_index(drop=False)
            
        #----------------------------------------------------------------
        # TWEET DATA
        #----------------------------------------------------------------
        tweet_id = tweet['id']
        
        # Cleanup tweet text, and convert emoji to text
        if 'extended_tweet' in tweet:
            y = tweet['extended_tweet']['full_text']
        else:
            y = tweet['text']
        
        y = y.encode('utf-8').decode('utf-8')
        y = emoji.demojize(y)
        #y = slugify(y)

        if tweet['coordinates'] is not None:
            z = tweet['coordinates']['coordinates']
            long = z[0]
            lat = z[1]
        else:
            z = None

        #-------------------------------------------------------------------
        # CLEAN HTML TAGS - get source application of Tweet
        #-------------------------------------------------------------------
        clean = re.compile('<.*?>')
        a = re.sub(clean, '', tweet['source'])


        #-------------------------------------------------------------------
        # CLEAN HASHTAGS - cycle through list of dictionaries
        #-------------------------------------------------------------------
        hash_list = tweet['entities']['hashtags']
        htags = []
        if not(hash_list == []):
            for ht in hash_list:
                htags.append(ht['text'])


        #-------------------------------------------------------------------
        # CLEAN MENTIONS - cycle through list of dictionaries
        #-------------------------------------------------------------------
        mention_list = tweet['entities']['user_mentions']
        mentions = []
        if not(mention_list == []):
            for um in mention_list:                
                mentions.append(um['screen_name'])

        
        
        tweet_record = [
            { 'id':tweet['id'],
              'tweet_date':tweet['timestamp_ms'], #datetime.fromtimestamp(tweet['timestamp_ms']),
              'tweet_text':y,
              'latitude':lat,
              'longitude':long,
              'reply_count':tweet['reply_count'],
              'retweet_count':tweet['retweet_count'],
              'source':a,
              'hashtags':htags,
              'mentions':mentions,
              'favourites_count':tweet['favorite_count'],
              'user_id':tweet['user']['id']
              }
            ]
        
        source_df = pd.DataFrame(tweet_record)
        source_df['tweet_date'] = pd.to_datetime(source_df['tweet_date'], unit='ms')

        # check if tweet exists in dataframe
        if not (tweet_df['id'] == tweet_id).any():
            # insert record in dataframe
            tweet_df = tweet_df.append(source_df)
        

    except:
        # if error, continue to next record
        continue

print(len(user_df.index))
print(len(tweet_df.index))

user_df.to_csv(r'twitter_users.csv', index=False)
tweet_df.to_csv(r'twitter_tweets.csv', index=False)
