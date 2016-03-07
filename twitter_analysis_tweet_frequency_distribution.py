import sys
import json
import operator
import matplotlib.pyplot as plt

#frequency distribution              

def main(tweetFile):
  tweet_file = open(tweetFile)                        # Open the file for reading
  tweet_hash = {}                                     # Define a dictionary for keeping the hashtags as keys and their frequency as values
  for tweet_line in tweet_file:                       # Loop for every tweet in the tweets file
    tweet = json.loads(tweet_line)                    # convert the json string to dictionary object
    if "entities" in tweet.keys():                    # Check whether entities tags present
      hashtags = tweet["entities"]["hashtags"]        #  - if present then extract the hashtags
      for ht in hashtags:                             # For every hashtag get the hashtag text value
        if ht != None:                                
          if ht["text"].encode("utf-8") in tweet_hash.keys():  # Check whether hashtag already in dictionary
            tweet_hash[ht["text"].encode("utf-8")] += 1        # - If it is then increment its frequency by 1 
          else:
            tweet_hash[ht["text"].encode("utf-8")] = 1         # - Else initialise the hashtag with frequency as 1
 
  sortedHashTags = dict(sorted(tweet_hash.items(), key=operator.itemgetter(1), reverse=True)[:10]) # Filter the top ten tweets  
                                                                                                   # - based on the frequency(descending order)
  print("HashTag Name   -   Frequency\n\n")                                                        
  for key,value in sorted(sortedHashTags.items(), key=lambda kv: (kv[1],kv[0]),reverse=True):      # sort the dictionary on the basis of frequency   
    print("#%s -  %d" % (key.decode("utf-8"), value))   

 # plt.plot(sortedHashTags, tweet_hash) 
#  plt.show()                                         # - and print the result

    
if __name__ == '__main__':
  if len(sys.argv) == 2:
    main(sys.argv[1])
  else:
    print('Usage: python sentiment_analysis.py stream_modi.json')
    print(' here stream_modi.json is a text file with live tweets from twitter in json format each tweet separated by a new line ')
