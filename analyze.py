import os
import sys
import json
import time
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

from datetime import datetime

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
		followers_file = open("users/" + curr_user_id,"r")
		following_list = followers_file.read().splitlines()
		for following in following_list:
			if following in previous_retweeters:
				seen_from.append(following)
					
		data['seen_from'] = seen_from
		previous_retweeters.append(curr_user_id)
		data_list.append(data)
	
	#returns with earliest tweet as entry 0
	return list(reversed(data_list))

def graph_tweets_vs_time(data_list):
	time_ms = [d['time_ms'] for d in data_list]
	x = time_ms
	y = []
	
	for i in range(0,len(time_ms)):
		y.append(i)
	
	plt.plot(x,y)
	plt.show()
	
def graph_previous_views_vs_time(data_list):
	time_ms = [d['time_ms'] for d in data_list]
	seen_from_list = [d['seen_from'] for d in data_list]
	x = time_ms
	y = []
	
	for i in range(0,len(time_ms)):
		y.append(len(seen_from_list[i]))
	
	plt.plot(x,y)
	plt.show()
	
def graph_followers_vs_time(data_list):
	time_ms = [d['time_ms'] for d in data_list]
	followers_list = [d['user']["followers_count"] for d in data_list]
	x = time_ms
	y = []
	
	for i in range(0,len(time_ms)):
		y.append(followers_list[i])
	
	plt.plot(x,y)
	plt.show()
	
if __name__ == "__main__":
	file_name = sys.argv[1]
	#gen_network_from_tweets(file_name)
	data_list = gen_network_from_tweets(file_name)
	graph_followers_vs_time(data_list)
	#ms_from_created_at("Sat Jun 17 03:05:08 +0000 2017")
	