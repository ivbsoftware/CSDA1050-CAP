#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import time

#Variables that contains the user credentials to access Twitter API
# Insert your own twitter developer user credentials
consumer_key = 'consumer_key'
consumer_secret = 'consumer_secret'
access_token = 'access_token'
access_token_secret = 'access_token_secret'


#This is a basic listener that just prints received tweets to stdout.
class SListener(StreamListener):
    
    def on_data(self, data):
        print(data)
        return True

    def on_error(self, status):
        print(status)


if __name__ == '__main__':
    # To run, from command line python twitter_stream_post.py > file_to_store_tweets.txt
    # will run until connection lost, or stopped CTRL+C

    #This handles Twitter authetification and the connection to Twitter Streaming API
    listen = SListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, listen)

    #This line filter Twitter Streams to capture data by Toronto polygon
    # GEO polygon from Oakville to Whitby  
    stream.filter(locations=[-79.639319,43.403221, -78.905820,43.855401])
        

    
