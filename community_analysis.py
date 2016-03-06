import tweepy
from tweepy import OAuthHandler
 
consumer_key = 'i54fIljKBTLPrp7sEg9nh7ZSZ'
consumer_secret = 'NSxZHzg0zkvFGxtjlmJ09Prx0u0rpxWYl1UO5lxIl6sbcepBCB'
access_token = '1201081159-Bwev81uKRnbAUeeRrd2CidpBMcFB68Xuni9WH3v' #Sujay's twitter account
access_secret = '8551xRS8cY73N6cBUoVgbMBPqTdNJ70oAIFGL9VbZLt5W'
 
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)

for status in tweepy.Cursor(api.home_timeline).items(10):
    # Process a single status
    print(status.text)