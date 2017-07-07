import os
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
		except tweepy.RateLimitError as e:
			print("******sleeping until more requests available (16 min)*******")
			print("current time: " + datetime.now().strftime('%Y-%m-%d_%H:%M:%S'))
			time.sleep(60*16)
			print("resuming")
			return self.timeout_safe_call(twitter_call, twitter_args)
			
		except tweepy.TweepError as e:
			print(e)
			return -2
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
		if(str(user_name) not in indexed_users):
			following_list = tweepy.Cursor(self.api.friends_ids, id=user_name, count=5000).items()
			output_file = open("users/" + str(user_name), "w")
			i = 0
			while True:
				user = self.timeout_safe_call(following_list.next)
				if user == -1:
					break
				if user == -2:
					print("can not access user")
					output_file.close()
					#os.remove("users/" + str(user_name))
					break
				output_file.write(str(user) + "\n")
					
		#else:
			#print("user already indexed")
		
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
		Tweet = None
		
		while True:
		
			while not StreamListener.get_data():
				pass
			
			already_seen_tweets = [f for f in listdir("tweet_searches") if isfile(join("tweet_searches", f))]
			tweet = StreamListener.get_data()[0]
			
			if str(tweet["retweeted_status"]["retweet_id"]) not in already_seen_tweets:
				output_file = "tweet_searches/" + str(tweet["retweeted_status"]["retweet_id"])
				self.tweet_parser.save_tweets_json(tweet, output_file)
				break
		
		return tweet
		
	def trace_retweets(self, tweet):
		print("finding past tweets with:")
		print(tweet["text"])
		tweets = self.search_past_tweets(tweet["text"])
		print(len(tweets))
		output_file = "tweet_search_results/" + datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
		self.tweet_parser.save_tweets_json(tweets, output_file)
	
	def init_stream_search(self, search_term):
		self.Stream.filter(lang="en", track=[seach_term], async=True)
	
	def search_past_tweets(self, seach_term): 
		tweet_iterator = tweepy.Cursor(self.api.search, q=seach_term, lang="en").items()
		filtered_tweets = []
		while True:
			tweet = self.timeout_safe_call(tweet_iterator.next)
			if tweet == -1:
				break
			filtered_tweet = self.tweet_parser.parse_tweet(tweet)
			filtered_tweets.append(filtered_tweet)
			
		return filtered_tweets
