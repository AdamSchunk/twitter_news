'''TODO:
1) pick a hashtag
2) find the first instance of the #
3) find who retweeted it from where
4) find who started the hashtag or who used it independently
5) generate the network based on this data


'''

import sys
from twitter_tools import Twitter_Tools

if __name__ == "__main__":
	tweet_thresh = int(sys.argv[2])
	query = sys.argv[1]
	tt = Twitter_Tools()
	tweet = tt.get_tweet_with_num_retweets(query, tweet_thresh)
	tt.trace_retweets(tweet)