import os
import sys
import json
import time
import math
import matplotlib
import statistics
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

from datetime import datetime
from numpy import linalg as LA
from collections import Counter
from scipy.stats import spearmanr
from twitter_tools import Twitter_Tools
from sklearn.preprocessing import normalize


def gen_network_graph_from_tweets(tweet_file):
	input = open(tweet_file, "r")
	tweets = json.load(input)
	users = []
	nodes = set()
	graph = nx.Graph()

	for tweet in tweets:
		users.append(tweet["user"]["id"])
		graph.add_node(tweet["user"]["id"])
	
	
	for curr_user in users:
		following_file = open("users/" + str(curr_user) + "_is_following","r")
		following_list = following_file.read().splitlines()
		for following in following_list:
			following_int = int(following)
			if graph.has_node(following_int):
				graph.add_edge(curr_user, following_int)
				
	for curr_user in users:
		followers_file = open("users/" + str(curr_user) + "_followers","r")
		followers_list = followers_file.read().splitlines()
		for followers in followers_list:
			followers_int = int(followers)
			if graph.has_node(followers_int):
				graph.add_edge(curr_user, followers_int)
	
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
		
		previous_retweeters.append(curr_user_id)
		data_list.append(data)
	#returns with earliest tweet as entry 0
	return list(reversed(data_list))

def graph_tweets_vs_time(data_list, file_name):
	directory = "analysis/images/tweets_vs_time/"
	
	if not os.path.exists(directory):
		os.makedirs(directory)
	
	if os.path.exists(directory + file_name):
		print("tweets vs time already saved")
		
	
	start_time = data_list[0]["time_ms"]
	time_ms = [(d['time_ms'] - start_time)/(1000*3600) for d in data_list]
	x = time_ms
	y = []
	
	for i in range(0,len(time_ms)):
		y.append(i)
	
	plt.plot(x,y)
	
	fig, ax1 = plt.subplots()
	ax1.plot(x, y, 'b-')
	ax1.set_xlabel("Hours")
	# Make the y-axis label, ticks and tick labels match the line color.
	ax1.set_ylabel('Tweets', color='b')
	ax1.tick_params('y', colors='b')
	
	return [fig,ax1]
	
	#plt.savefig(directory + file_name)
	#plt.clf()
	
def graph_followers_vs_time_segmented(data_list, file_name):
	directory = "analysis/images/followers_vs_time_segmented/"
	if not os.path.exists(directory):
		os.makedirs(directory)
	time_ms = [d['time_ms'] for d in data_list]
	followers_count_list = [d['user']["followers_count"] for d in data_list]
	
	y = []
	
	interval = (3600*1000) #hour/x
	
	section_time = time_ms[0]
	follow_cnt = 0
	for i, followers in enumerate(followers_count_list):
		time = time_ms[i]
		
		if time >= section_time + interval:
			y.append(follow_cnt)
			follow_cnt = 0
			section_time = section_time + interval
			
		follow_cnt = follow_cnt + followers
		
		
	#for num_followers in followers_count_list:
	#	y.append(num_followers)
	
	x = np.linspace(1,len(y),len(y))
	
	plt.plot(x,y)
	plt.savefig(directory + "/" + file_name)
	plt.clf()
	
def graph_followers_vs_time_segmented_log(data_list, file_name):
	directory = "analysis/images/followers_vs_time_segmented/"
	if not os.path.exists(directory):
		os.makedirs(directory)
	time_ms = [d['time_ms'] for d in data_list]
	followers_count_list = [d['user']["followers_count"] for d in data_list]
	
	y = []
	
	interval = (3600*1000) #hour/x
	
	section_time = time_ms[0]
	follow_cnt = 0
	for i, followers in enumerate(followers_count_list):
		time = time_ms[i]
		
		if time >= section_time + interval:
			y.append(follow_cnt)
			follow_cnt = 0
			section_time = section_time + interval
			
		follow_cnt = follow_cnt + followers
		
		
	#for num_followers in followers_count_list:
	#	y.append(num_followers)
	
	x = np.linspace(1,len(y),len(y))
	
	plt.plot(x,y)
	plt.savefig(directory + "/" + file_name)
	plt.clf()
	
def graph_followers_vs_time(data_list, file_name):
	directory = "analysis/images/followers_vs_time/"
	if not os.path.exists(directory):
		os.makedirs(directory)
	start_time = data_list[0]["time_ms"]
	time_ms = [(d['time_ms'] - start_time)/(1000*3600) for d in data_list]
	followers_count_list = [d['user']["followers_count"] for d in data_list]
	x = time_ms
	y = followers_count_list #seriously? who coded this shit... oh right it was me... Bad adam!
	
	#for num_followers in followers_count_list:
	#	y.append(num_followers)
	
	plt.plot(x,y)
	plt.savefig(directory + "/" + file_name)
	plt.clf()
	
def graph_following_vs_time(data_list, file_name):
	directory = "analysis/images/following_vs_time/"
	if not os.path.exists(directory):
		os.makedirs(directory)
	start_time = data_list[0]["time_ms"]
	time_ms = [(d['time_ms'] - start_time)/(1000*3600) for d in data_list]
	followers_count_list = [d['user']["friends_count"] for d in data_list]
	x = time_ms
	y = followers_count_list #seriously? who coded this shit... oh right it was me... Bad adam!
	
	#for num_followers in followers_count_list:
	#	y.append(num_followers)
	
	plt.plot(x,y)
	plt.savefig(directory + "/" + file_name)
	plt.clf()
	
def graph_followers_vs_time_log(data_list, file_name):
	directory = "analysis/images/followers_vs_time_log/"
	if not os.path.exists(directory):
		os.makedirs(directory)
	start_time = data_list[0]["time_ms"]
	time_ms = [(d['time_ms'] - start_time)/(1000*3600) for d in data_list]
	followers_count_list = [1+(d['user']["followers_count"]/10000) for d in data_list]
	y = followers_count_list
	x = time_ms
	
	#for num_followers in followers_count_list:
	#	y.append(num_followers)
	
	fig1, ax1 = plt.subplots()
	ax1.plot(x,y)
	plt.xlabel("Hours")
	plt.ylabel("Log Followers")
	ax1.set_yscale('log')
	ax1.set_yticks([1, 10, 100])
	ax1.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())

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
	
	#if os.path.exists(directory + file_name):
		#print("degree vs time already saved")
		#return
		
		
	time_ms = [d['time_ms'] for d in data_list]	
	users = [d["user"]["id"] for d in data_list]
	x = time_ms
	y = []
	
	for user in users:
		deg = nx.degree(graph, user)
		#if deg == 0:
		#	print(user)
		y.append(deg)
		
	plt.plot(x,y)
	
	
	plt.savefig(directory + file_name)
	plt.clf()
		
def graph_in_out_degree_ratio_vs_time(graph, data_list, file_name):
	directory = "analysis/images/degree_ratio_vs_time/"
	if not os.path.exists(directory):
		os.makedirs(directory)
	
	#if os.path.exists(directory + file_name):
		#print("degree vs time already saved")
		#return
		
		
	time_ms = [d['time_ms'] for d in data_list]	
	users = [d["user"]["id"] for d in data_list]
	followers_count_list = [d['user']["followers_count"] for d in data_list]
	x = time_ms
	y = []
	
	for i,user in enumerate(users):
		deg = nx.degree(graph, user)
		foll = followers_count_list[i]
		if foll != 0:
			y.append(deg/foll)
		else:
			y.append(0)
		
	plt.plot(x,y)
	
	
	plt.savefig(directory + file_name)
	plt.clf()
	
def graph_avg_diam_vs_time(graph, data_list, file_name, window_size):
	fig, ax1 = graph_tweets_vs_time(data_list, file_name)
	directory = "analysis/images/diam_vs_time/"
	if not os.path.exists(directory):
		os.makedirs(directory)
	
	if os.path.exists(directory + file_name):
		pass
		#return
		
	
	start_time = data_list[0]["time_ms"]
	time_ms = [(d['time_ms'] - start_time)/(1000*3600) for d in data_list]
	times_to_remove = []
	users = [d["user"]["id"] for d in data_list]
	x = time_ms
	y = []
	y_end = []
	max_dist = 0
	dists_l = []
	missing_points = []
	for i, user in enumerate(users):
		dists = []
		err_val = 0
		
		if i+window_size > len(users):
			continue
			
		window = users[i:i+window_size]
		for prev_user in window:
			for j in range(0,window_size):
				cur = window[j]
				try:
					dist = len(nx.shortest_path(graph, cur, prev_user))
					if(dist == 0):
						print(cur)
						print(prev_user)
					dists.append(dist)
				except:
					dists.append(err_val)
		max_dist = max([max_dist, max(dists)])
		
		missing_points.append(Counter(dists)[0])
		
		dists_l.append(dists)
		
	for dists in dists_l:
		for i, dist in enumerate(dists):
			if dist == err_val:
				dists[i] = max_dist
		y.append(sum(dists)/len(dists))

	y = y+y_end
		
	avg = sum(dists_l[0])/len(dists_l[0])
	for i, avg_dist in enumerate(y):
		if avg_dist == err_val:
			y[i] = avg

	avgw = 10
	tmp = [avg]* (avgw-1)
	y = tmp + y
	
	ax2 = ax1.twinx()
	ax2.plot(x[:-1*window_size+1],moving_average(y, avgw), color="r")
	ax2.set_ylabel('Diameter', color='r')
	ax2.tick_params('y', colors='r')

	fig.tight_layout()
	plt.savefig(directory + file_name)
	plt.clf()
	
	#plt.plot(x,missing_points)
	#plt.savefig(directory + "missing_" + file_name)
	
	return [x, y]
	
def corel_avg_diam_vs_time(graph):
	data_dir = "tweet_search_results/"
	data_dir = "C:\\Users\\adamschunk\\git\\Network-Generator-and-Analysis\\NetworkGenerator\\100000_cluster1000\\runs"
	window_user_size_l = [5,10,25]
	window_time_size_l = [1/12,1/2,1,2] #x*hour
	#window_time_size_l = [x *(3600*1000) for x in window_time_size_l]
	
	
	
	for window_user_size in window_user_size_l:
		print("usr: " + str(window_user_size))
		for window_time_size in window_time_size_l:
			windows = []  
			diam_avgs = []
			retweet_rates = []
			print("min: " + str(window_time_size*60))
			for file in os.listdir(data_dir):	
				if not "timeSteps.csv" in file:
					continue
				
				
				
				
				
				curr_tweet_rates = []
				flag = False
				for i,diam in enumerate(cur_diam_list):
					start_time = cur_time_list[i]
					end_time = start_time + window_time_size
					if flag:
						break
					j = i
					tweets_in_window = 0
					while cur_time_list[j] < end_time and not flag:
						tweets_in_window += 1
						j += 1
						if j >= len(cur_time_list)-1:
							flag = True
					curr_tweet_rates.append(tweets_in_window)
					
				for i in range(0,len(curr_tweet_rates)):
					diam_avgs.append(cur_diam_list[i])
					retweet_rates.append(curr_tweet_rates[i])
				
			print(spearmanr(diam_avgs,retweet_rates)[0])
			print()	
				
	
def moving_average(a, n=10) :
	ret = np.cumsum(a, dtype=float)
	ret[n:] = ret[n:] - ret[:-n]
	return ret[n - 1:] / n
	
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
				dists.append(len(nx.shortest_path(graph, user, large_node["user"]["id"])))
				#print("path found")
			except:
				dists.append(50-len(dists))
		
		if large_nodes:
			#print(dists)
			closest = dists.index(min(dists))
			delta_ts.append(time_ms[i]- large_nodes[closest]["time_ms"] )
		else:
			delta_ts.append(0)
		
		if num_followers >= avg_followers + std*2:
			#print("new large node")
			large_nodes.append(data_list[i])
			
	print(len(large_nodes))
	max_dt = max(delta_ts)
	min_dt = min(delta_ts)
	
	dt_norm = []
	
	for dt in delta_ts:
		dt_norm.append((dt-min_dt)/(max_dt-min_dt))

	
	for i in range(len(x)):
		plt.plot([x[i]],[y[i]], marker = 'o', color=(dt_norm[i], 0, dt_norm[i]))
	
	plt.savefig(directory + file_name)
	plt.clf()			
				
def graph_avg_follower(data_list, file_name):
	directory = "analysis/images/avg_follower/"
	if not os.path.exists(directory):
		os.makedirs(directory)
	time_ms = [d['time_ms'] for d in data_list]
	followers_count_list = [d['user']["followers_count"] for d in data_list]
	x = time_ms
	y = []
	
	for i in range(0,len(followers_count_list)):
		y.append(sum(followers_count_list[i-5:i+5])/10)
	
	plt.plot(x,y)
	plt.savefig(directory + "/" + file_name)
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

def predict_on_degree(data_list, file_name):
	directory = "analysis/images/predict_on_followers/"
	if not os.path.exists(directory):
		os.makedirs(directory)
	
	#if os.path.exists(directory + file_name):
	#	print("follower based prediction already saved")
	#	return
		
	
	followers_count_list = [d['user']["followers_count"] for d in data_list]
	
	time_ms = [d['time_ms'] for d in data_list]
	x = time_ms #range(0,len(data_list))
	y = []
	avgs = []
	stds = []
	
	#make a rolling func? every time it sees something near 5000 it gets larger and then gets smaller again 
	#might be good...
	
	curr = 0
	prev_binary = []
	for i in range(0,len(time_ms)):
		#(1/(1+math.exp(-((followers_count_list[i]-10000)/100)))-.1)*100
		
		s = sum(prev_binary[-50:])/50
		
		if followers_count_list[i] > 6000:
			res = max(s+.80,.1)
			prev_binary.append(1)
		else:
			res = min(s-.15,0)
			prev_binary.append(0)
		
		curr += res
		curr = max(curr, 0)
		y.append(curr)
	
	#average (unlikely to likely) but the std should play a large roll in that measure. small std with decent average should also count
	#5000 avg seems to corrolate well
	
	plt.plot(x,y)
	plt.savefig(directory + file_name)
	plt.clf()
		
def printClustering(graph):
	print(graph.number_of_edges())
	print(len(graph))
	
def file_len(fname):
	i = 0
	with open(fname) as f:
		for i, l in enumerate(f):
			pass	
	return i + 1
	
def printGeneralNetworkStats():
	num_large = 0
	num_small = 0
	large_users = 0
	small_users = 0
	large_following = []
	large_followers = []
	small_following = []
	small_followers = []
	missing = 0
	
	
	
	for file in os.listdir("tweet_search_results"):
		tweets = json.load(open("tweet_search_results/" + file, "r"))
		users = json.load(open("users/dict.txt", "r"))
		isLarge = len(tweets) > 1500
		if isLarge:
			num_large += 1
		else:
			num_small += 1
			
		
		for tweet in tweets:
			user_id = tweet["user"]["id"]
			try:
				num_followers = users[str(user_id)]["followers_count"]
				num_following = users[str(user_id)]["friends_count"]
				
			except Exception as e:
				print(e)
				missing += 1
				continue
				
			if isLarge:
				large_users += 1
				large_following.append(num_following)
				large_followers.append(num_followers)
			else:
				small_users += 1
				small_following.append(num_following)
				small_followers.append(num_followers)
		
	print("large following: " + str(np.percentile(large_following, 25)) + ", " + 
		str(np.percentile(large_following, 50)) + ", " + str(np.percentile(large_following, 75)) + ", " + 
		str(np.percentile(large_following, 95)))
	
		
	print("large followers: " + str(np.percentile(large_followers, 25)) + ", " + 
		str(np.percentile(large_followers, 50)) + ", " + str(np.percentile(large_followers, 75)) + ", " + 
		str(np.percentile(large_followers, 95)))
		
	print("small following: " + str(np.percentile(small_following, 25)) + ", " + 
		str(np.percentile(small_following, 50)) + ", " + str(np.percentile(small_following, 75)) + ", " + 
		str(np.percentile(small_following, 95)))
		
	print("small followers: " + str(np.percentile(small_followers, 25)) + ", " + 
		str(np.percentile(small_followers, 50)) + ", " + str(np.percentile(small_followers, 75)) + ", " + 
		str(np.percentile(small_followers, 95)))
	
	print(num_large)
	print(num_small)
	
	print(large_users)
	print(small_users)
	
	print(max(large_following))
	print(max(large_followers))
	print(max(small_following))
	print(max(small_followers))
	
def average_follower_degree():
	tt = Twitter_Tools()
	follower_counts = []
	for file in os.listdir("users"):
		print("hi")
		content = open("users/" + file, "r").readlines()
		content = [x.strip() for x in content] 
		for user_name in content:
			
			usr = tt.timeout_safe_call(tt.api.get_user, user_name)
			if type(usr) == int:
				continue
			
			target = usr.followers_count
			follower_counts.append(target)

		
		follower_counts_np = np.sort(follower_counts) 

		p25 = follower_counts_np[int(len(follower_counts_np)/4)]
		p50 = follower_counts_np[int(len(follower_counts_np)/2)]
		p75 = follower_counts_np[int(len(follower_counts_np)*3/4)]
			
		print(len(follower_count))
		print(str(p25) + ", " + str(p50) + ", " + str(p75))
		
def makeLargeUserFile():
	data_dir = "tweet_search_results/"
	output = open("users/dict.txt", "w")
	users = {}
	for file in os.listdir(data_dir):
		print(file)
		input = open(data_dir + file, "r")
		tweets = json.load(input)
		for tweet in tweets:
			users[str(tweet["user"]["id"])] = tweet["user"]
	json.dump(users, output, indent = 4, sort_keys = True)

	
def run_based_analysis():
	data_dir = "tweet_search_results/"
	
	window_user_size_l = [5,10,25,50]
	window_time_size_l = [1/12,1/2,1,2] #x*hour
	window_time_size_l = [x *(3600*1000) for x in window_time_size_l]
	
	max_follower = 0
	
	for file in os.listdir(data_dir):
		data_list = gen_network_from_tweets(data_dir + file)
		followers_count_list = [d['user']["followers_count"] for d in data_list]
		max_follower = np.log10(max([max(followers_count_list), max_follower]))
		
	print(max_follower)
		
	for window_user_size in window_user_size_l:
		print("usr: " + str(window_user_size))
		for window_time_size in window_time_size_l:
			windows = []  
			print("min: " + str(window_time_size/(60*1000)))
			for file in os.listdir(data_dir):
				data_list = gen_network_from_tweets(data_dir + file)
				time_ms = [d['time_ms'] for d in data_list]
				followers_count_list = [d['user']["followers_count"] for d in data_list]
				num_users = len(followers_count_list)
				
				user_idx = 0
				while user_idx != -1:
					user_window = []
					time_window = []
					
					time_idx = user_idx
					if time_idx >= num_users:
						break
					
					user_window = followers_count_list[user_idx:user_idx + window_user_size]
					user_window = [np.log10(1+x/1000) for x in user_window]
					section_start_time = time_ms[time_idx]
					
					
					time_idx_end = time_idx
					while time_ms[time_idx_end] < section_start_time + window_time_size:
						time_idx_end += 1
						if time_idx_end >= num_users:
							user_idx = -1
							break
							
					time_window = time_ms[time_idx : time_idx_end]
							
					if user_idx != -1:
						windows.append([user_window, time_window])
						user_idx += 1
					
			max_f = [max(windows[i][0]) for i in range(0,len(windows))]
			median_f = [np.median(windows[i][0]) for i in range(0,len(windows))]
			average_f = [np.average(windows[i][0])  for i in range(0,len(windows))]
			num_tweets_in_window = [len(windows[i][1]) for i in range(0,len(windows))]
				
			#print(max_f)
			#print(spearmanr(max_f,num_tweets_in_window)[0])
			print(spearmanr(average_f,num_tweets_in_window)[0])
			print()
				
			
	
	return
		
	
if __name__ == "__main__":
	data_dir = "tweet_search_results/"
	analysis_dir = "analysis/"

	#corel_avg_diam_vs_time()
	
	edges = []
	G = nx.Graph()
	with open('from_java/edges.csv', 'r') as f:
		edges = [line.rstrip('\n').split(",") for line in f]
	
	for edge in edges:
		#Gd.add_edge(int(edge[0]), int(edge[1]))
		G.add_edge(int(edge[0]), int(edge[1]))
	
	for file in os.listdir(data_dir):
		print(file)
		pass
		#print(file)
		#graph = gen_network_graph_from_tweets(data_dir + file)
		data_list = gen_network_from_tweets(data_dir + file)
		#printClustering(graph)
		#graph_tweets_vs_time(data_list, file + ".png")
		#graph_followers_vs_time(data_list, file + ".png")
		#graph_following_vs_time(d	ata_list, file + ".png")
		#graph_followers_vs_time_log(data_list, file + ".png")
		#graph_followers_vs_time_segmented(data_list, file + ".png")
		#graph_avg_follower(data_list, file + ".png")
		#predict_on_degree(data_list, file + ".png")
		#graph_degree_vs_time(graph, data_list, file + ".png")
		#graph_in_out_degree_ratio_vs_time(graph, data_list, file + ".png")
		#graph_clustering_vs_time(graph, data_list, file + "png")
		graph_avg_diam_vs_time(G, data_list, file + ".png", 50)
		#analyze_high_follower_nodes(graph, data_list, file + ".png")
		