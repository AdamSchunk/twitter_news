'''TODO:
1) pick a hashtag
2) find the first instance of the #
3) find who retweeted it from where
4) find who started the hashtag or who used it independently
5) generate the network based on this data


'''

import sys
from twitter_tools import Twitter_tools

if __name__ == "__main__":
	hashtag = sys.argv[1]
	tt = Twitter_tools()
	tt.get_hashtag_to_json(sys.argv[1], 1, "output.txt")