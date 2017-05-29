import csv
import sys
import time
import json
import tweepy

from tweet_parser import Tweet_Parser
from tweet_stream_listener import Tweet_Stream_Listener

class Twitter_Tools(object):

	def __init__(self):
		# Variables that contains the user credentials to access Twitter API 
		ACCESS_TOKEN = '860191806465744897-2FaIqC3FEjqc2BnhqNsjXuYN34AEjuR'
		ACCESS_SECRET = '9rV4BEatXoOfPYoiUSvUgQ7zeRuevlQEQb6xux4FT2HKT'
		CONSUMER_KEY = '82Md1jsxRDwx8kWD1BqKucpaZ'
		CONSUMER_SECRET = 'zLLAeZ3LxfSJP8HSbuFg02Lo9V7aTqbPLuLfr1dp0Y8wwFa6Du'

		auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
		auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
		self.api = tweepy.API(auth)
		self.tweet_parser = Tweet_Parser()
		
		

	def timeout_safe_call(self, twitter_call, twitter_args = None):
		try:
			if twitter_args is None:
				res = twitter_call()
			elif isinstance(twitter_args, tuple):
				res = twitter_call(*twitter_args)
			else:
				res = twitter_call(twitter_args)
		except tweepy.TweepError:    
			print("******sleeping until more requests available (15 min)*******")
			for i in range(0,15): 
				print("\n****" + str(15-i) + "min remaining****") 
				for j in range(0,61): #yes this is longer than 1 minute, but the 15 second buffer prevents this from running twice
					time.sleep(1)
					sys.stdout.write(str(j+1)+' ')
					sys.stdout.flush()
			print("resuming")
			return self.timeout_safe_call(twitter_call, twitter_args)
		except StopIteration:
			return -1
			
		return res
			
	def get_user_is_following(self, user_name):
		user = self.api.get_user(user_name)
		print(user_name + "is following")
		following_list = tweepy.Cursor(self.api.friends, id=user_name).items()
		while True:
			following = self.timeout_safe_call(following_list.next)
			if following == -1:
				break
			print(following.screen_name)
		
	def get_is_following_user(self, user_name):
		user = self.api.get_user(user_name)
		print("Friends of: " + user_name)
		followers_list = tweepy.Cursor(self.api.followers, id=user_name).items()
		while True:
			follower = self.timeout_safe_call(followers_list.next)
			if follower == -1:
				break
			print(follower.screen_name)
			
	def get_num_user_followers(self, username):
		user = api.get_user(user_name)
		return user.followers_count
		
	def get_num_user_following(self, username):
		user = self.api.get_user(user_name)
		return user.friends_count

	def find_tweet_with_num_retweets(self, query, tweet_thresh):
		StreamListener = Tweet_Stream_Listener(query, 0, tweet_thresh)
		Stream = tweepy.Stream(auth=self.api.auth, listener = StreamListener)
		Stream.filter(track=[query], async=True)
		
		while not StreamListener.get_data():
			pass
		
		tweet = StreamListener.get_data()[0]
		print(tweet)
		return tweet
		
	def trace_retweets(self, tweet):
		print("finding past tweets")
		tweets = self.search_past_tweets(tweet["text"])
		print(len(tweets))
		self.tweet_parser.save_tweets_json(tweets, "output.txt")
	
	def init_stream_search(self, search_term):
		self.Stream.filter(track=[seach_term], async=True)
	
	def search_past_tweets(self, seach_term): 
		tweet_iterator = tweepy.Cursor(self.api.search, q=seach_term, lang="en").items()
		filtered_tweets = []
		i = 0
		while True:
			i += 1
			if 1%100 == 0:
				print( str(i) + " tweets found")
			tweet = self.timeout_safe_call(tweet_iterator.next)
			if tweet == -1:
				break
			filtered_tweet = self.tweet_parser.parse_tweet(tweet)
			filtered_tweets.append(filtered_tweet)
			
		return filtered_tweets
