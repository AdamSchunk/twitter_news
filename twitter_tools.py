import csv
import sys
import time
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
	num_following = 0
	following_list = tweepy.Cursor(api.friends, id=user_name).items()
	while True:
		following = timeout_safe_call(following_list.next)
		if following == -1:
			break
		num_following += 1
		print(str(num_following) + ": " + following.screen_name)
	
def get_user_followers(user_name):
	user = api.get_user(user_name)
	print("Friends of: " + user_name)
	num_following = 0
	followers_list = tweepy.Cursor(api.followers, id=user_name).items()
	while True:
		follower = timeout_safe_call(followers_list.next)
		if follower == -1:
			break
		num_following += 1
		print(str(num_following) + ": " + follower.screen_name)
		
def get_num_user_followers(username):
	user = api.get_user(user_name)
	return user.followers_count
	
def get_num_user_following(username):
	user = api.get_user(user_name)
	return user.friends_count

#def get_hashtag(hashtag, num_tweets): 
#	for tweet in tweepy.Cursor(api.search, q=hashtag, count=num_tweets, lang="en", since_id=1996).items():
#		print(tweet.created_at, tweet.text)
		#csvWriter.writerow([tweet.created_at, tweet.text.encode('utf-8')])
		