import csv
import sys
import time
import json
import tweepy

class Twitter_tools(object):

	def __init__(self):
		# Variables that contains the user credentials to access Twitter API 
		ACCESS_TOKEN = '860191806465744897-2FaIqC3FEjqc2BnhqNsjXuYN34AEjuR'
		ACCESS_SECRET = '9rV4BEatXoOfPYoiUSvUgQ7zeRuevlQEQb6xux4FT2HKT'
		CONSUMER_KEY = '82Md1jsxRDwx8kWD1BqKucpaZ'
		CONSUMER_SECRET = 'zLLAeZ3LxfSJP8HSbuFg02Lo9V7aTqbPLuLfr1dp0Y8wwFa6Du'

		auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
		auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
		self.api = tweepy.API(auth)

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

	def get_hashtag_to_json(self, hashtag, num_tweets, output_file): 
		output = open(output_file, "w")
		tst_outpuut = open("sample_tweet.txt", "w")
		tweet_iterator = tweepy.Cursor(self.api.search, q=hashtag, lang="en").items(num_tweets)
		buff = []
		
		#fields wanted:
		# hashtag section
		# in reply to
		# retweet count
		# retweet status -- might be original 
		
		while True:
			tweet = self.timeout_safe_call(tweet_iterator.next)
			if tweet == -1:
				break
			print(type(tweet))
			tst_outpuut.write(json.dumps(tweet._json, indent = 4, sort_keys=True))

			tweet_dict = tweet._json
			
			filtered_tweet = {}
			filtered_tweet["text"] = tweet_dict["text"]
			filtered_tweet["in_reply_to_screen_name"] = tweet_dict["in_reply_to_screen_name"]
			filtered_tweet["retweet_count"] = tweet_dict["retweet_count"]
			filtered_tweet["retweeted"] = tweet_dict["retweeted"]

			user_dict = tweet_dict["user"]
			filtered_user = {}
			filtered_user["screen_name"] = user_dict["screen_name"]
			filtered_user["followers_count"] = user_dict["followers_count"]
			filtered_user["friends_count"] = user_dict["friends_count"]
			
			
			filtered_retweet = {}
			if "retweeted_status" in tweet_dict.keys():
				retweet_dict = tweet_dict["retweeted_status"]
				filtered_retweet["retweet_count"] = retweet_dict["retweet_count"]
				filtered_retweet["retweeted_from"] = retweet_dict["user"]["screen_name"]
			
			
			
			filtered_tweet["retweeted_status"] = filtered_retweet
			filtered_tweet["user"] = filtered_user
			
			output.write(json.dumps(filtered_tweet, indent = 4, sort_keys=True))
		