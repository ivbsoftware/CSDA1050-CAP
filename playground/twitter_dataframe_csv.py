import json
import pandas as pd
import matplotlib.pyplot as plt

tweets_data_path = 'toronto_twitter_data.txt'

# read the data into an array 
tweets_data = []
tweets_file = open(tweets_data_path, "r") #.read()
for line in tweets_file:
    try:
        tweet = json.loads(line)

        # FLATTEN DATA
        # store the user data in their own columns
        tweet['user_screen_name'] = tweet['user']['screen_name']
        tweet['user_verfied'] = tweet['user']['verified']
        tweet['user_followers_count'] = tweet['user']['followers_count']
        tweet['user_friends_count'] = tweet['user']['friends_count']
        tweet['user_favourites_count'] = tweet['user']['favourites_count']
        tweet['user_statuses_count'] = tweet['user']['statuses_count']
        tweet['user_language'] = tweet['user']['lang']
        tweet['user_display_name'] = tweet['user']['name']

        # Check if this is a 140+ character tweet
        if 'extended_tweet' in tweet:
            # Store the extended tweet text in 'extended_tweet-full_text'
            tweet['extended_tweet-full_text'] = tweet['extended_tweet']['full_text']
        else:
            tweet['extended_tweet-full_text'] = tweet['text']
    
        if 'retweeted_status' in tweet:
            # Store the retweet user screen name in 'retweeted_status-user-screen_name'
            tweet['retweeted_status-user-screen_name'] = tweet['retweeted_status']['user']['screen_name']

            # Store the retweet text in 'retweeted_status-text'
            tweet['retweeted_status-text'] = tweet['retweeted_status']['text']

        tweet['country'] = tweet['place']['country']
        tweet['location_name'] = tweet['place']['full_name']

        if tweet['place']['place_type'] == 'city':
            tweet['location_city'] = tweet['place']['name']
            
        tweet['user_location_name'] = tweet['user']['location']

        if tweet['geo'] is not None:
            tweet['coord'] = tweet['geo']['coordinates']
        else:
            tweet['coord'] = None
                  
        
        tweets_data.append(tweet)
    except:
        continue


# print the number of tweets
print (len(tweets_data))

# structure the tweets data into a pandas DataFrame
tweets = pd.DataFrame(tweets_data)

tweets.to_csv(r'twitter_dataframe3.csv')
