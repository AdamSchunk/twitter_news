'''TODO:
1) pick a hashtag
2) find the first instance of the #
3) find who retweeted it from where
4) find who started the hashtag or who used it independently
5) generate the network based on this data


'''

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
	
	
if __name__ == "__main__":
	tweet_thresh = int(sys.argv[2])
	query = sys.argv[1]
	tt = Twitter_Tools()
	tweet = tt.find_tweet_with_num_retweets(query, tweet_thresh)
	tt.trace_retweets(tweet)
	gen_network_from_tweets("output.txt")