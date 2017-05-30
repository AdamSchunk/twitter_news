import tweepy

from tweet_parser import Tweet_Parser

class Tweet_Stream_Listener(tweepy.StreamListener):
	
	def __init__(self, query, mode=1, tweet_thresh=0):
		#modes:
		# 0: search
		# 1: save
		super(self.__class__, self).__init__()
		self.query = query
		self.mode = mode
		self.tweet_thresh = tweet_thresh
		self.tweet_parser = Tweet_Parser()
		self.data = []
	
	def on_status(self, status):
		filtered_tweet = self.tweet_parser.parse_tweet(status)
		num_retweets = int(filtered_tweet["retweeted_status"]["retweet_count"])
		if (self.mode == 0 and num_retweets >= self.tweet_thresh and num_retweets <= self.tweet_thresh * 1.25):
			self.data.append(filtered_tweet)
			#print(filtered_tweet)
			return False
		
	def on_error(self, status_code):
		if status_code == 420:
			print("streaming api call limit reached")
			#TODO deal with this case and make it more robust
			return False
		
	
	def get_data(self):
		return self.data
			
	