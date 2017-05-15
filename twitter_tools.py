import csv
import sys
import time
import json
import tweepy

# Variables that contains the user credentials to access Twitter API 
ACCESS_TOKEN = '860191806465744897-2FaIqC3FEjqc2BnhqNsjXuYN34AEjuR'
ACCESS_SECRET = '9rV4BEatXoOfPYoiUSvUgQ7zeRuevlQEQb6xux4FT2HKT'
CONSUMER_KEY = '82Md1jsxRDwx8kWD1BqKucpaZ'
CONSUMER_SECRET = 'zLLAeZ3LxfSJP8HSbuFg02Lo9V7aTqbPLuLfr1dp0Y8wwFa6Du'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

def timeout_safe_call(twitter_call, twitter_args = None):
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
		return timeout_safe_call(twitter_call, twitter_args)
	except StopIteration:
		return -1
		
	return res
		
def get_user_following(user_name):
	user = api.get_user(user_name)
	print("Friends of: " + user_name)
	following_list = tweepy.Cursor(api.friends, id=user_name).items()
	while True:
		following = timeout_safe_call(following_list.next)
		if following == -1:
			break
		print(str(num_following) + ": " + following.screen_name)
	
def get_user_followers(user_name):
	user = api.get_user(user_name)
	print("Friends of: " + user_name)
	followers_list = tweepy.Cursor(api.followers, id=user_name).items()
	while True:
		follower = timeout_safe_call(followers_list.next)
		if follower == -1:
			break
		print(str(num_following) + ": " + follower.screen_name)
		
def get_num_user_followers(username):
	user = api.get_user(user_name)
	return user.followers_count
	
def get_num_user_following(username):
	user = api.get_user(user_name)
	return user.friends_count

def get_hashtag_to_json(hashtag, num_tweets, output_file): 
	output = open(output_file, "w")
	tweet_iterator = tweepy.Cursor(api.search, q=hashtag, lang="en").items(num_tweets)
	buff = []
	while True:
		tweet = timeout_safe_call(tweet_iterator.next)
		filtered_tweet = 
		if tweet == -1:
			break
		output.write(json.dumps(tweet._json, indent = 4, sort_keys=True))
			
get_hashtag_to_json("ccmm", 1, "output.txt")
		