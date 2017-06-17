import csv
import sys
import time
import json
import tweepy


from os import listdir
from os.path import isfile, join
from datetime import datetime
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
			print("******sleeping until more requests available (16 min)*******")
			print("current time: " + datetime.now().strftime('%Y-%m-%d_%H:%M:%S'))
			time.sleep(60*16)
			print("resuming")
			return self.timeout_safe_call(twitter_call, twitter_args)
		except StopIteration:
			return -1
			
		return res
			
	def print_tweets_from_user(self, user_name):
		user = self.api.get_user(user_name)
		for status in tweepy.Cursor(self.api.user_timeline, id=user_name).items(10):
			tweet = self.tweet_parser.parse_tweet(status)
			print(tweet)
		
			
	def save_user_is_following(self, user_name):
		indexed_users = [f for f in listdir("users") if isfile(join("users", f))]
		if(user_name not in indexed_users):
			output_file = open("users/" + str(user_name), "w")
			following_list = tweepy.Cursor(self.api.friends_ids, id=user_name, count=5000).items()
			while True:
				user = self.timeout_safe_call(following_list.next)
				if user == -1:
					break
				output_file.write(str(user) + "\n")
		
	def get_is_following_user(self, user_name):
		print("Friends of: " + user_name)
		followers_list = tweepy.Cursor(self.api.followers_ids, id=user_name, count=5000).items()
		i = 0
		while True:
			user = self.timeout_safe_call(followers_list.next)
			if user == -1:
				break
			i = i+1
			print(i)
			

	def find_tweet_with_num_retweets(self, query, tweet_thresh):
		StreamListener = Tweet_Stream_Listener(query, 0, tweet_thresh)
		Stream = tweepy.Stream(auth=self.api.auth, listener = StreamListener)
		Stream.filter(track=[query], async=True)
		
		while not StreamListener.get_data():
			pass
		
		already_seen_tweets = [f for f in listdir("tweet_searches") if isfile(join("tweet_searches", f))]
		tweet = StreamListener.get_data()[0]
		
		if tweet["retweeted_status"]["retweet_id"] not in already_seen_tweets:
			output_file = "tweet_searches/" + str(tweet["retweeted_status"]["retweet_id"])
			self.tweet_parser.save_tweets_json(tweet, output_file)
		
		return tweet
		
	def trace_retweets(self, tweet):
		print("finding past tweets")
		tweets = self.search_past_tweets(tweet["text"])
		print(len(tweets))
		output_file = "tweet_search_results/" + datetime.now().strftime('%Y-%m-%d_%H-%M')
		self.tweet_parser.save_tweets_json(tweets, output_file)
	
	def init_stream_search(self, search_term):
		self.Stream.filter(lang="en", track=[seach_term], async=True)
	
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
