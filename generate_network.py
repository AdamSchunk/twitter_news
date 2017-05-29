'''TODO:
1) pick a hashtag
2) find the first instance of the #
3) find who retweeted it from where
4) find who started the hashtag or who used it independently
5) generate the network based on this data


'''

import sys
import json
from twitter_tools import Twitter_Tools

if __name__ == "__main__":
	tweet_thresh = int(sys.argv[2])
	query = sys.argv[1]
	tt = Twitter_Tools()
	tweet = tt.find_tweet_with_num_retweets(query, tweet_thresh)
	tt.trace_retweets(tweet)
	
	
def gen_network_from_tweets(tweet_file):
	input = open(tweet_file, "r")
	tweets = json.loads(output)
	users = set()
	for tweet in tweets:
		users.add(tweet["user"]["screen_name"])
		users.add(tweet["retweeted_status"]["retweeted_from"]
		
		#use networkx for all of the netwrork stuff
	