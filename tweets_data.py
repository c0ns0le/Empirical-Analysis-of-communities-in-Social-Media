from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import re
import sys
import json
import dateutil.parser
from pytz import timezone
import pytz

# The consumer keys can be found on your application's Details
# page located at https://dev.twitter.com/apps (under "OAuth settings")
CONSUMER_KEY = 'i54fIljKBTLPrp7sEg9nh7ZSZ'
CONSUMER_SECRET = 'NSxZHzg0zkvFGxtjlmJ09Prx0u0rpxWYl1UO5lxIl6sbcepBCB'

# The access tokens can be found on your applications's Details
# page located at https://dev.twitter.com/apps (located
# under "Your access token")
ACCESS_TOKEN = '1201081159-Bwev81uKRnbAUeeRrd2CidpBMcFB68Xuni9WH3v'
ACCESS_TOKEN_SECRET = '8551xRS8cY73N6cBUoVgbMBPqTdNJ70oAIFGL9VbZLt5W'

sgtz = timezone('Asia/Kolkata')
utc = pytz.timezone('UTC')

STATIONS = [
        'Bangalore',
        'Delhi',
        'Chennai',
        'Mumbai',
        'Kolkata',
        'Hyderabad',
        'Chandigarh'
        ]
regex = re.compile('|'.join(STATIONS).lower())
linenum_re = re.compile(r'([A-Z][A-Z]\d+)')
retweets_re = re.compile(r'^RT\s')

enc = lambda x: x.encode('latin1', errors='ignore')

class StdOutListener(StreamListener):
    def on_data(self, data):

        tweet = json.loads(data)

        if not tweet.has_key('user'):
            print 'No user data - ignoring tweet.'
            return True

        user = enc(tweet['user']['name'])
        text = enc(tweet['text'])

        # ignore text that doesn't contain one of the keywords
        matches = re.search(regex, text.lower())
        if not matches:
            return True

        # ignore retweets
        if re.search(retweets_re, text):
            return True

        location = enc(tweet['user']['location'])
        source = enc(tweet['source'])
        d = dateutil.parser.parse(enc(tweet['created_at']))

        # localize time
        d_tz = utc.normalize(d)
        localtime = d.astimezone(sgtz)
        tmstr = localtime.strftime("%Y%m%d-%H:%M:%S")

        # append the hourly tweet file
        with open('tweets-%s.data' % tmstr.split(':')[0], 'a+') as f:
            f.write(data)

        # is this a geocoded tweet?
        geo = tweet['geo']
        if geo and geo['type'] == 'Point':
            # collect location of    station
            coords = geo['coordinates']
            ln = re.search(linenum_re, text)
            if ln:
                with open('station_locations.csv', 'a+') as mrtgeo:
                    print("Found geo coords for Stations (%s) '%s': (%f, %f)\n" %
                            (ln.group(), matches.group(), coords[1], coords[0]))
                    mrtgeo.write("%f\t%f\t%s\t%s\n" %
                            (coords[1], coords[0], matches.group(), ln.group()))

        # print summary of tweet
        print('%s\n%s\n%s\n%s\n%s\n\n ----------------\n' % (user, location, source, tmstr, text))


        return True

    def on_error(self, status):
        print('status: %s' % status)

if __name__ == '__main__':
    l = StdOutListener()
    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    stream = Stream(auth, l, timeout=60)

    print("Listening to filter stream...")

    stream.filter(track=STATIONS)