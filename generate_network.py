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
import networkx as nx
import matplotlib.pyplot as plt


from twitter_tools import Twitter_Tools
	
	
	
def gen_network_from_tweets(tweet_file):
	input = open(tweet_file, "r")
	tweets = json.load(input)
	nodes = set()
	graph = nx.Graph()
	edges = []
	for tweet in tweets:
		retweeter = tweet["user"]["screen_name"]
		retweeted = tweet["retweeted_status"]["retweeted_from"]
		nodes.add(retweeter)
		nodes.add(retweeted)
		edges.append([retweeted, retweeter])
	
	for node in nodes:
		graph.add_node(node)
		
	for edge in edges:
		graph.add_edge(edge[0],edge[1])
	
	print("drawing graph")
	nx.draw(graph)
	plt.show()
	#use networkx for all of the netwrork stuff
	
def generate_retweet_files():
	tweet = tt.find_tweet_with_num_retweets(query, tweet_thresh)
	if tweet:
		tt.trace_retweets(tweet)
	else:
		print("tweet already seen" + str(tweet["retweeted_status"]["id"]))
		

def gen_new_user_files():
	for retweets_file in os.listdir("tweet_search_results"):
		retweet_list_file = open("tweet_search_results/" + retweets_file, "r")
		retweet_list = json.load(retweet_list_file)
		for retweet in retweet_list:
			tt.save_user_is_following(retweet["user"]["id"])

		
if __name__ == "__main__":
	tweet_thresh = int(sys.argv[2])
	query = sys.argv[1]
	tt = Twitter_Tools()
	generate_retweet_files()
	gen_new_user_files()
	#gen_network_from_tweets("output.txt")