import json
import re

class Tweet_Parser(object):

	def save_tweets_json(self, tweets, output_file):
		output = open(output_file, "w")
		output.write(json.dumps(tweets, indent = 4, sort_keys=True))
	
	def load_tweets_json(self, file):
		retweet_file = open("tweet_search_results/" + file, "r")
		return json.load(retweet_list_file)
		 
	
	def add_tweets_to_file(self, tweets, output_file):
		output = open(output_file, "r")
		old_data = json.loads(output)
		tweets = old_data + tweets
		output.close()
		
		output = open(output_file, "w")
		output.write(json.dumps(tweets, indent = 4, sort_keys=True))
		
	def format_text(self, text):
		text = re.sub(r'https?:\/\/.*[\r\n]*', '', text, flags=re.MULTILINE)
		text = re.sub(r'^RT ', '', text, flags=re.MULTILINE)
		return(text)
	
	def parse_tweet(self, unfiltered_tweet):
	
		#fields wanted:
		# hashtag section
		# in reply to
		# retweet count
		# retweet status -- might be original 
		
		tweet_dict = unfiltered_tweet._json
		
		filtered_tweet = {}
		filtered_tweet["id"] = tweet_dict["id"]
		filtered_tweet["created_at"] = tweet_dict["created_at"]
		filtered_tweet["text"] = self.format_text(tweet_dict["text"])
		
		filtered_tweet["in_reply_to_screen_name"] = tweet_dict["in_reply_to_screen_name"]
		filtered_tweet["retweet_count"] = tweet_dict["retweet_count"]
		filtered_tweet["retweeted"] = tweet_dict["retweeted"]

		filtered_user = {}
		filtered_user["id"] = tweet_dict["user"]["id"]
		filtered_user["screen_name"] = tweet_dict["user"]["screen_name"]
		filtered_user["followers_count"] = tweet_dict["user"]["followers_count"]
		filtered_user["friends_count"] = tweet_dict["user"]["friends_count"]
		
		
		filtered_retweet = {}
		if "retweeted_status" in tweet_dict.keys():
			filtered_retweet["retweet_id"] = tweet_dict["retweeted_status"]["id"]
			filtered_retweet["retweet_count"] = tweet_dict["retweeted_status"]["retweet_count"]
			filtered_retweet["retweeted_from"] = tweet_dict["retweeted_status"]["user"]["screen_name"]
		
		else:
			filtered_retweet["retweet_count"] = 0
			filtered_retweet["retweeted_from"] = ""
		
		
		
		filtered_tweet["retweeted_status"] = filtered_retweet
		filtered_tweet["user"] = filtered_user
			
		return filtered_tweet