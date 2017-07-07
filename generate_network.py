'''TODO:
1) pick a hashtag
2) find the first instance of the #
3) find who retweeted it from where
4) find who started the hashtag or who used it independently
5) generate the network based on this data


'''

import os
import sys
import json
import time
import networkx as nx
import matplotlib.pyplot as plt



from twitter_tools import Twitter_Tools
	
	
	
def gen_network_from_tweets(tweet_file):
	input = open(tweet_file, "r")
	tweets = json.load(input)
	users = []
	nodes = set()
	graph = nx.Graph()
	edges = []

	for tweet in tweets:
		users.append(str(tweet["user"]["id"]))
		graph.add_node(str(tweet["user"]["id"]))
	
	
	for curr_user in users:
		followers_file = open("users/" + str(curr_user),"r")
		following = followers_file.read().splitlines()
		for potentially_following in users:
			if potentially_following in following:
				graph.add_edge(curr_user, potentially_following)
	
	nx.write_edgelist(graph, "test.edgelist")
	#use networkx for all of the netwrork stuff
	
def generate_retweet_files(num_files, query, tweet_thresh):
	for i in range(num_files):
		tweet = tt.find_tweet_with_num_retweets(query, tweet_thresh)
		if tweet:
			tt.trace_retweets(tweet)
			time.sleep(15)
		else:
			print("tweet already seen" + str(tweet["retweeted_status"]["id"]))
		
		
		
#generates new users based on 
#new retweet files found by the search system
def gen_new_user_files():
	completed_file_list = os.listdir("completed_retweet_files")
	for retweet_file in os.listdir("tweet_search_results"):
	
		if(retweet_file in completed_file_list):
			print("users in " + retweet_file + " already indexed")
			continue
		print(retweet_file)
		retweet_list_file = open("tweet_search_results/" + retweet_file, "r")
		retweet_list = json.load(retweet_list_file)
		for retweet in retweet_list:
			tt.save_user_is_following(retweet["user"]["id"])
			#print(retweet["user"]["id"])
		
		open("completed_retweet_files/" + retweet_file, "w")

		
		
		
if __name__ == "__main__":
	tweet_thresh = int(sys.argv[2])
	query = sys.argv[1]
	tt = Twitter_Tools()
	#generate_retweet_files(4, query, tweet_thresh)
	#tt.save_user_is_following("34051134")	
	gen_new_user_files()
	
	#gen_network_from_tweets(query)