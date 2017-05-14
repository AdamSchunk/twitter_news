import tweepy
import csv

# Variables that contains the user credentials to access Twitter API 
ACCESS_TOKEN = '860191806465744897-2FaIqC3FEjqc2BnhqNsjXuYN34AEjuR'
ACCESS_SECRET = '9rV4BEatXoOfPYoiUSvUgQ7zeRuevlQEQb6xux4FT2HKT'
CONSUMER_KEY = '82Md1jsxRDwx8kWD1BqKucpaZ'
CONSUMER_SECRET = 'zLLAeZ3LxfSJP8HSbuFg02Lo9V7aTqbPLuLfr1dp0Y8wwFa6Du'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

# Open/Create a file to append data
csvFile = open('tweets.csv', 'a')
#Use csv Writer
csvWriter = csv.writer(csvFile)

def get_user_following(user_name):
	user = api.get_user(user_name)
	print("Friends of: " + user_name)
	num_friends = 0
	for friend in tweepy.Cursor(api.friends, id=user_name).items():
		num_friends += 1
		print(friend.screen_name)
	print(num_friends)
	
def get_user_followers(user_name):
	user = api.get_user(user_name)
	print("Friends of: " + user_name)
	num_friends = 0
	for friend in tweepy.Cursor(api.followers, id=user_name).items():
		num_friends += 1
		print(friend.screen_name)
	print(num_friends)

def get_hashtag(hashtag, num_tweets): 
	for tweet in tweepy.Cursor(api.search, q=hashtag, count=num_tweets, lang="en", since_id=1996).items():
		print(tweet.created_at, tweet.text)
		#csvWriter.writerow([tweet.created_at, tweet.text.encode('utf-8')])
		
get_user_followers("jbensal")