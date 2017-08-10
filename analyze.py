import os
import sys
import json
import time
import math
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

from datetime import datetime

def gen_network_graph_from_tweets(tweet_file):
	input = open(tweet_file, "r")
	tweets = json.load(input)
	users = []
	nodes = set()
	graph = nx.Graph()
	edges = []

	for tweet in tweets:
		users.append(tweet["user"]["id"])
		graph.add_node(tweet["user"]["id"])
	
	
	for curr_user in users:
		following_file = open("users/" + str(curr_user),"r")
		following_list = following_file.read().splitlines()
		for following in following_list:
			following_int = int(following)
			if graph.has_node(following_int):
				graph.add_edge(curr_user, following_int)
	
	return graph
	#use networkx for all of the netwrork stuff

def month_num_from_str(month):
	month = month.lower()
	m = {
        'jan': 1,
        'feb': 2,
        'mar': 3,
        'apr':4,
         'may':5,
         'jun':6,
         'jul':7,
         'aug':8,
         'sep':9,
         'oct':10,
         'nov':11,
         'dec':12
        }
	out = m[month]
	return out

def ms_from_created_at(created_at):
	sections = created_at.split()
	hms = sections[3]
	month = str(month_num_from_str(sections[1]))
	day = sections[2]
	year = sections[5]
	time_str = (day + " " + month + " " + year + " " + hms)
	date_time = datetime.strptime(time_str, "%d %m %Y %H:%M:%S")
	
	return date_time.timestamp()*1000

def gen_network_from_tweets(tweet_file):
	input = open(tweet_file, "r")
	tweets = json.load(input)

	data_list = []
	previous_retweeters = []
	for tweet in tweets:
		data = {}
		curr_user_id = str(tweet["user"]["id"])
		
		data['user'] = tweet["user"]
		data['time_ms'] = ms_from_created_at(tweet["created_at"])
		
		#generate list of who they could have seen the tweet from
		seen_from = []
		following_file = open("users/" + curr_user_id,"r")
		following_list = following_file.read().splitlines()
		for following in following_list:
			if following in previous_retweeters:
				seen_from.append(following)
					
		data['seen_from'] = seen_from
		previous_retweeters.append(curr_user_id)
		data_list.append(data)
		following_file.close()
	#returns with earliest tweet as entry 0
	return list(reversed(data_list))

def graph_tweets_vs_time(data_list, file_name):
	directory = "analysis/images/tweets_vs_time/"
	
	if not os.path.exists(directory):
		os.makedirs(directory)
	
	if os.path.exists(directory + file_name):
		print("tweets vs time already saved")
		return
	
	time_ms = [d['time_ms'] for d in data_list]
	x = time_ms
	y = []
	
	for i in range(0,len(time_ms)):
		y.append(i)
	
	plt.plot(x,y)
	plt.savefig(directory + file_name)
	plt.clf()
	
def graph_previous_views_vs_time(data_list, file_name):
	time_ms = [d['time_ms'] for d in data_list]
	seen_from_list = [d['seen_from'] for d in data_list]
	x = time_ms
	y = []
	
	for i in range(0,len(time_ms)):
		y.append(len(seen_from_list[i]))
	
	plt.plot(x,y)
	plt.show()
	
def graph_followers_vs_time(data_list, file_name):
	directory = "analysis/images/followers_vs_time/"
	if not os.path.exists(directory):
		os.makedirs(directory)
	time_ms = [d['time_ms'] for d in data_list]
	followers_count_list = [d['user']["followers_count"] for d in data_list]
	x = time_ms
	y = []
	
	for num_followers in followers_count_list:
		y.append(num_followers)
	
	plt.plot(x,y)
	plt.savefig(directory + "/" + file_name)
	plt.clf()
	
def graph_clustering_vs_time(graph, data_list, file_name):
	directory = "analysis/images/clustering_vs_time/"
	if not os.path.exists(directory):
		os.makedirs(directory)
		
	time_ms = [d['time_ms'] for d in data_list]	
	users = [d["user"]["id"] for d in data_list]
	x = time_ms
	y = []
	
	for user in users:
		y.append(nx.clustering(graph,user))
		
	plt.plot(x,y)
	plt.savefig(directory + file_name)
	plt.clf()
	
def graph_degree_vs_time(graph, data_list, file_name):
	directory = "analysis/images/degree_vs_time/"
	if not os.path.exists(directory):
		os.makedirs(directory)
	
	if os.path.exists(directory + file_name):
		print("degree vs time already saved")
		return
		
		
	time_ms = [d['time_ms'] for d in data_list]	
	users = [d["user"]["id"] for d in data_list]
	x = time_ms
	y = []
	
	for user in users:
		y.append(nx.degree(graph, user))
		
	plt.plot(x,y)
	
	
	plt.savefig(directory + file_name)
	plt.clf()
	
def graph_avg_diam_vs_time(graph, data_list, file_name):
	directory = "analysis/images/diam_vs_time/"
	if not os.path.exists(directory):
		os.makedirs(directory)
	
	if os.path.exists(directory + file_name):
		pass
		#return
		
		
	time_ms = [d['time_ms'] for d in data_list]	
	times_to_remove = []
	users = [d["user"]["id"] for d in data_list]
	x = time_ms[1:]
	y5 = []
	prev_users = [users[0]]
	for i, user in enumerate(users[1:]):
		dists = []
		#if nx.degree(graph, user) == 0:
		#	times_to_remove.append(i)
		#	continue
		for prev_user in prev_users[-10:]:
			try:
				dist = len(nx.shortest_path(graph, user, prev_user))
			except:
				dist = len(users)
			dists.append(dist)

			
		y5.append(sum(dists)/len(dists))
		prev_users.append(user)
		
	#for time in sorted(times_to_remove, reverse=True):
	#	del x[time]
		
	plt.plot(x,y5)
	
	
	plt.savefig(directory + file_name)
	plt.clf()
	
def analyze_high_follower_nodes(graph, data_list, file_name):

	directory = "analysis/images/followers_tweets_vs_time/"
	if not os.path.exists(directory):
		os.makedirs(directory)
		
	time_ms = [d['time_ms'] for d in data_list]
	followers_count_list = [d['user']["followers_count"] for d in data_list]
	users = [d["user"]["id"] for d in data_list]
	x = time_ms
	y = []
	
	for i in range(0,len(time_ms)):
		y.append(i)
	
	large_nodes = []
		
	avg_followers = sum(followers_count_list)/len(followers_count_list)
	std = np.std(followers_count_list)

	delta_ts = []
	
	for i, user in enumerate(users):
		num_followers = followers_count_list[i]
		dists = []
		for large_node in large_nodes:
			try:
				dists.append(len(nx.shortest_path(graph, user, prev_user)))
			except:
				dists.append(len(users))
		
		if large_nodes:
			closest = dists.index(min(dists))
			delta_ts.append(time_ms[i]- large_nodes[closest]["time_ms"] )
		else:
			delta_ts.append(1)
		
		if num_followers >= avg_followers + std*2:
			large_nodes.append(data_list[i])
			
	
	max_dt = max(delta_ts)
	min_dt = min(delta_ts)
	
	dt_norm = []
	
	for dt in delta_ts:
		print(dt)
		dt_norm.append((dt-min_dt)/(max_dt-min_dt))

	
	for i in range(len(x)):
		plt.plot([x[i]],[y[i]], marker = 'o', color=(dt_norm[i], 0, dt_norm[i]))
	
	plt.savefig(directory + file_name)
	plt.clf()			
		
		
	
	
def find_jumps(x, y, data_list):
	slopes = []
	for i, tweet in enumerate(y[1:]):
		slopes.append((y[i]-y[i-1])/(x[i]-x[i-1]))

	for i, slope in enumerate(slopes):
		pass
	
def analyze_jumps(graph, data_list, file_name): #look at who retweeted from the large nodes
	#TODO: work on this funciton
	directory = "analysis/images/jump_analysis/"
	if not os.path.exists(directory):
		os.makedirs(directory)
	
	if os.path.exists(directory + file_name):
		print("degree vs time already saved")
		return
		
		
	time_ms = [d['time_ms'] for d in data_list]
	x = time_ms
	y = []
	
	for i in range(0,len(time_ms)):
		y.append(i)


if __name__ == "__main__":
	data_dir = "tweet_search_results/"
	analysis_dir = "analysis/"
	for file in os.listdir(data_dir):
		print(file)
		graph = gen_network_graph_from_tweets(data_dir + file)
		data_list = gen_network_from_tweets(data_dir + file)
		graph_tweets_vs_time(data_list, file + ".png")
		#graph_degree_vs_time(graph, data_list, file + ".png")
		#graph_clustering_vs_time(graph, data_list, file + "png")
		#graph_avg_diam_vs_time(graph, data_list, file + ".png")
		#graph_followers_vs_time(data_list, file + ".png")
		analyze_high_follower_nodes(graph, data_list, file + ".png")
	