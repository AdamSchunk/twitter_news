# Import the necessary package to process data in JSON format
try:
	import json
except ImportError:
	import simplejson as json

# Import the necessary methods from "twitter" library
from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream

# Variables that contains the user credentials to access Twitter API 
ACCESS_TOKEN = '860191806465744897-2FaIqC3FEjqc2BnhqNsjXuYN34AEjuR'
ACCESS_SECRET = '9rV4BEatXoOfPYoiUSvUgQ7zeRuevlQEQb6xux4FT2HKT'
CONSUMER_KEY = '82Md1jsxRDwx8kWD1BqKucpaZ'
CONSUMER_SECRET = 'zLLAeZ3LxfSJP8HSbuFg02Lo9V7aTqbPLuLfr1dp0Y8wwFa6Du'

oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

# Initiate the connection to Twitter Streaming API
twitter_stream = TwitterStream(auth=oauth)

# Get a sample of the public data following through Twitter
iterator = twitter_stream.statuses.sample()

# Print each tweet in the stream to the screen 
# Here we set it to stop after getting 1000 tweets. 
# You don't have to set it to stop, but can continue running 
# the Twitter API to collect data for days or even longer. 
tweet_count = 10
for tweet in iterator:
	tweet_count -= 1
	# Twitter Python Tool wraps the data returned by Twitter 
	# as a TwitterDictResponse object.
	# We convert it back to the JSON format to print/score
	output_file = open("tweet_output.txt", "w")
	output_file.write(json.dumps(tweet) + "\n")
	print(json.dumps(tweet))
	
	# The command below will do pretty printing for JSON data, try it out
	# print json.dumps(tweet, indent=4)
	   
	if tweet_count <= 0:
		break 