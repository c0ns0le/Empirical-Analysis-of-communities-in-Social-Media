# Import the required libraries.
import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
import pandas as pd
import matplotlib.pyplot as plt

# Make the graphs prettier
pd.set_option('display.mpl_style', 'default')

consumerKey = 'i54fIljKBTLPrp7sEg9nh7ZSZ'
consumerSecret = 'NSxZHzg0zkvFGxtjlmJ09Prx0u0rpxWYl1UO5lxIl6sbcepBCB'
access_token = '1201081159-Bwev81uKRnbAUeeRrd2CidpBMcFB68Xuni9WH3v'
access_secret = '8551xRS8cY73N6cBUoVgbMBPqTdNJ70oAIFGL9VbZLt5W'

#Use tweepy.OAuthHandler to create an authentication using the given key and secret
auth = tweepy.OAuthHandler(consumer_key=consumerKey, consumer_secret=consumerSecret)

#Connect to the Twitter API using the authentication
api = tweepy.API(auth)
auth.set_access_token(access_token, access_secret)

#stream = Stream(auth)
#Perform a basic search query where we search for the '#Oscars2015' in the tweets
result = api.search(q='%23ChennaiRainsHelp') #%23 is used to specify '#'

# Print the number of items returned by the search query to verify our query ran. Its 15 by default
len(result)

tweet = result[0] #Get the first tweet in the result

# Analyze the data in one tweet to see what we require
for param in dir(tweet):
#The key names beginning with an '_' are hidden ones and usually not required, so we'll skip them
    if not param.startswith("_"):
        print "%s : %s\n" % (param, eval('tweet.'+param))


results = []

#Get the first 5000 items based on the search query
for tweet in tweepy.Cursor(api.search, q='%23ChennaiRainsHelp').items(5000):
    results.append(tweet)

# Verify the number of items returned
print len(results)

# Create a function to convert a given list of tweets into a Pandas DataFrame.
# The DataFrame will consist of only the values, which I think might be useful for analysis...


def toDataFrame(tweets):

    DataSet = pd.DataFrame()

    DataSet['tweetID'] = [tweet.id for tweet in tweets]
    DataSet['tweetText'] = [tweet.text for tweet in tweets]
    DataSet['tweetRetweetCt'] = [tweet.retweet_count for tweet in tweets]
    DataSet['tweetFavoriteCt'] = [tweet.favorite_count for tweet in tweets]
    DataSet['tweetSource'] = [tweet.source for tweet in tweets]
    DataSet['tweetCreated'] = [tweet.created_at for tweet in tweets]


    DataSet['userID'] = [tweet.user.id for tweet in tweets]
    DataSet['userScreen'] = [tweet.user.screen_name for tweet in tweets]
    DataSet['userName'] = [tweet.user.name for tweet in tweets]
    DataSet['userCreateDt'] = [tweet.user.created_at for tweet in tweets]
    DataSet['userDesc'] = [tweet.user.description for tweet in tweets]
    DataSet['userFollowerCt'] = [tweet.user.followers_count for tweet in tweets]
    DataSet['userFriendsCt'] = [tweet.user.friends_count for tweet in tweets]
    DataSet['userLocation'] = [tweet.user.location for tweet in tweets]
    DataSet['userTimezone'] = [tweet.user.time_zone for tweet in tweets]

    return DataSet

#Pass the tweets list to the above function to create a DataFrame
DataSet = toDataFrame(results)

# Let's check the top 5 records in the Data Set
DataSet.head(5)

# Similarly let's check the last 2 records in the Data Set
DataSet.tail(2)

# 'None' is treated as null here, so I'll remove all the records having 'None' in their 'userTimezone' column
DataSet = DataSet[DataSet.userTimezone.notnull()]

# Let's also check how many records are we left with now
len(DataSet)


# Count the number of tweets in each time zone and get the first 10
tzs = DataSet['userLocation'].value_counts()[:10]
print tzs



