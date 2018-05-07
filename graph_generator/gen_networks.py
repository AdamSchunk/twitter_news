import os
import re
import copy
import random
import math
import time
import json
import numpy as np
import matplotlib.pyplot as plt

'''
In my model the arrows point opposite from the paper referenced.
In the paper the A -> B represents A follows B
Here A -> B represents information flows from A to B (B follows A)
'''
def load_network(input_file):
	node_file = open("networks/" + input_file + "/nodes.csv", "r")
	edge_file = open("networks/" + input_file + "/edges.csv", "r")
	nodes_str = node_file.readlines()[1:]
	edges_str = edge_file.readlines()[1:]
	nodes = []
	edges = []
	for node_str in nodes_str:
		id, followers, following = node_str.split(",")
		nodes.append([int(followers), [], int(following), []])
		
	for edge_str in edges_str:
		node, follower, weight = edge_str.split(",")
		node = int(node)
		follower = int(follower)
		
		nodes[node][1].append(follower)
		nodes[follower][3].append(node)
	
	return nodes
		
def write_node_output(nodes, output_file):
	res = "id,num_following\n"
	for i,node in enumerate(nodes):
		
		res = res + str(i) + "," + str(node[0]) + "," + str(node[2]) + "\n"
		
	output = open(output_file + "/nodes.csv", "w")
	
	output.write(res)
	
def write_edge_output(nodes, output_file):
	all_edges = []
	res = "from,to,weight\n"

	for i, node in enumerate(nodes):
		for edge in node[1]:
			res = res + str(i) + "," + str(edge) + ",1\n"
		
		
	output = open(output_file + "/edges.csv", "w")
	
	output.write(res)	

	
#in degree of nodes from the paper (followers)
#out degree in generated graph
def degree_func(): 
	followers = 0
	x = [.0001, .00177, .31622, 10, 177.8, 562.3] #*10e4 (probability of getting y)
	#-8, -6.75, -4.75, -3, -1.75, -1.25
	y = [100000,10000,1000,100,10,1]
	r = random.uniform(.0031623, 562)
	for i, x1 in enumerate(x):
		if r <= x1:
			x_dis = (r-x[i-1])/(x[i]-x[i-1])
			followers = int(x_dis*(y[i-1]-y[i]) + y[i])
			break
	
	following = 0
	if followers <= 1000:
		following = followers * (1.2 - (.2*followers/1000)) + 3
		
	else:
		following = followers - (followers/2) * ((followers-1000)/100000)
	following = int(following)
	return followers, following
	
def gen_nodes(num):
	nodes = []
	for i in range(0,num):
		num_followers, num_following = degree_func()
		nodes.append([num_followers, [], num_following, []])
		
	return nodes
			
			
def weighted_choice(weights):
	total = sum(w for w in weights)
	r = random.uniform(0, total)
	upto = 0
	for i,w in enumerate(weights):
		if upto + w >= r:
			return i
		upto += w
	assert False, "Shouldn't get here"


def gen_edge_probs(nodes, curr_node_idx):
	weights = np.full(len(nodes), 100)
	curr_node_relationships = nodes[curr_node_idx][1] + list(set(nodes[curr_node_idx][3]) - set(nodes[curr_node_idx][1]))
	
	
	
	for i, node in enumerate(nodes):
		#generates weights for every possible connection based on max #following
		if i == curr_node_idx or i in nodes[curr_node_idx][1]: # if i is node, or is already following node
			weights[i] = 0
			continue
		deduct = 100*(len(nodes[i][3])/nodes[i][2]) #num_following/max_num_following
		weights[i] = weights[i] - min(deduct,90)
	
		#modifies weights based on # of shared connections
		tmp_rel = nodes[i][1] + list(set(nodes[i][3]) - set(nodes[i][1]))
		intersect = set(curr_node_relationships).intersection(tmp_rel)
		
		mult = 1+len(intersect)
		
		weights[i] = weights[i] * mult
		
	return weights
	
#generates edges, adds one follower (out arrow) to each node sequentially until
#no more followers are available in any node
def gen_edges(nodes):
	followers_available = np.full(len(nodes), True)
	total_nodes = len(nodes)
	percent_done = 0
	total_followers = sum([n[0] for n in nodes])
	num_done = 0
	while True in followers_available:
		for i, node in enumerate(nodes):
			if followers_available[i] == False:
				continue
				
			weights = gen_edge_probs(nodes, i)
			new_follower = weighted_choice(weights)
			
			nodes[i][1].append(new_follower)
			nodes[new_follower][3].append(i)
			followers_available[i] = len(nodes[i][1]) < nodes[i][0]
			
	
			#if there are fewer nodes than available connections.
			#this should not happen under normal operation. prevents errors in testing small networks
			if len(nodes[i][1]) == len(nodes)-1: 	
				followers_available[i] = False	
				
			num_done += 1 		
			if (num_done%int(total_followers/100) == 0): 
				print(str(int(num_done/total_followers*100)) + "%")
	
def tweet(nodes, node_idx, tweeted, seen, curr_step):
	tweeted[node_idx] = True
	for follower in nodes[node_idx][1]:
		seen[follower][0] = curr_step
		seen[follower][1] = seen[follower][1]+1
	
	
def run_network(nodes):
	tweeted = np.full(len(nodes), False)
	seen = np.full((len(nodes),2), 0)
	timesteps = []
	
	rand_start = 0
	while True:
		rand_start = random.randint(0,len(nodes)-1)
		if nodes[rand_start][0] <= 30:
			break
	tweet(nodes, rand_start, tweeted, seen, 1)
	
	count = 0
	curr_step = 1
	base_prob = .02
	while count < 5:
		timesteps.append(copy.deepcopy(tweeted))
		tweet_next = []
		for i in range(0, len(tweeted)):
			if not tweeted[i] and seen[i][0]:
				r = random.uniform(0,1)
				
				time_past = curr_step - seen[i][0] + 1
				
				prob = base_prob/(time_past*2)

				#prob =  1- math.pow((1-prob),seen[i][1])
				
				
				#prob = base_prob + (1-base_prob)/((curr_step - seen[i])) 
				
				#prob = base_prob + math.pow(time_past, 1.5)/30
				
				
				
				if r < max(prob, .000001):
					tweet_next.append(i)
		if not tweet_next:
			count += 1
		else:
			count = 0
			
		for tweeter in tweet_next:
			tweet(nodes, tweeter, tweeted, seen, curr_step)
		
		curr_step += 1
		
	return timesteps
			
def gen_net(n, output_dir):
	nodes = gen_nodes(n)
	edges = gen_edges(nodes)
	
	if not os.path.exists("networks/" + output_dir):
		os.makedirs("networks/" + output_dir)
	
	write_node_output(nodes, "networks/" + output_dir)
	write_edge_output(nodes, "networks/" + output_dir)
	
def run_analysis(timesteps, nodes, output_dir):
	output_dir = output_dir + "/" + str(int(time.time()))
	
	try:
		os.stat("networks/" + output_dir)
	except:
		os.mkdir("networks/" + output_dir) 
	
	x = np.linspace(0, len(timesteps)-1, len(timesteps), endpoint=True)
	y = []
	
	
	user_tweet_list = []
	new_user_tweet = []

	
	#plot tweets vs time
	for ts in timesteps:
		tweeted_this_ts=[i for i, x in enumerate(ts) if x]
		if not user_tweet_list:
			new_user_tweet.append([x for x in tweeted_this_ts]) #writing code on 2 hours of sleep makes bad code...
		else:
			new_user_tweet.append([x for x in tweeted_this_ts if x not in user_tweet_list[-1]])
			
		user_tweet_list.append(tweeted_this_ts)
		y.append(len(user_tweet_list[-1]))
		
		
	user_order_file = open("networks/" + output_dir + "/user_order.txt", "w")
	
	user_order_file.write(json.dumps(new_user_tweet, indent = 4, sort_keys=True))
	
	plt.plot(x,y)
	plt.savefig("networks/" + output_dir + "/tweets_over_time.png")
	plt.clf()
	
	
	
	#plot degree vs time
	y = []
	already_tweeted = []
	for count, ts in enumerate(timesteps):
		idxs = [i for i, j in enumerate(ts) if j == True]
		tmp = 0
		for idx in idxs:
			if idx not in already_tweeted:
				tmp = tmp + nodes[idx][0]
				already_tweeted.append(idx)
		
		y.append(tmp)
			
	#x = np.linspace(0, len(y)-1, len(y), endpoint=True)
	plt.plot(x,y)
	plt.savefig("networks/" + output_dir + "/followers_over_time_avg.png")
	plt.clf()
	
	
	#plot degree vs time
	y = []
	x = []
	already_tweeted = []
	for count, ts in enumerate(timesteps):
		idxs = [i for i, j in enumerate(ts) if j == True]
		tmp = []
		for idx in idxs:
			if idx not in already_tweeted:
				tmp.append(nodes[idx][0])
				already_tweeted.append(idx)
		
		num_x = len(tmp)
		for i, t in enumerate(tmp):
			y.append(t)
			x.append(count + i/num_x)
			
	#x = np.linspace(0, len(y)-1, len(y), endpoint=True)
	plt.plot(x,y)
	plt.savefig("networks/" + output_dir + "/followers_over_time.png")
	plt.clf()
	
	
def clustering(curr_node_idx, curr_node, nodes):
	nbrhood = curr_node[1] + list(set(curr_node[3]) - set(curr_node[1]))
	nbrhood.append(curr_node_idx)
	nbrhood_edgs = 0
	for n in nbrhood:		
		followers_in_rbrhood = set(nodes[n][1]).intersection(nbrhood)
		nbrhood_edgs = nbrhood_edgs + len(followers_in_rbrhood)
		
	num_neigh = len(nbrhood)
	
	return nbrhood_edgs/(num_neigh*(num_neigh-1))
		
		
def net_analysis(nodes, output):
	directory = "networks/" + output
	x = np.linspace(0, len(nodes)-1, len(nodes), endpoint=True)
	
	#follower degree
	deg = []
	y = []
	for n in nodes:
		y.append(n[0])
		deg.append(n[0])
	
	y.sort()
	plt.plot(x,y)
	plt.savefig(directory + "/follower_degree")
	plt.clf()
	
	#following degree
	y = []
	for n in nodes:
		y.append(n[2])
	
	y.sort()
	plt.plot(x,y)
	plt.savefig(directory + "/following_degree")
	plt.clf()
	
	#clustering
	y = []
	for i,n in enumerate(nodes):
		y.append(clustering(i, n, nodes))
	
	deg, y = (list(x) for x in zip(*sorted(zip(deg, y))))
	
	plt.plot(deg,y)
	plt.savefig(directory + "/clustering")
	plt.clf()
	
def run_from_save(output_name, num_runs):
	#add in to do multiple runs
	nodes = load_network(output_name)
	for i in range(0,num_runs):
		print(i)
		ts = run_network(nodes)
		while np.count_nonzero(ts[-1] == True) <= 300: # if less than x people tweeted, redo the analysis
			ts = run_network(nodes)
		start_idx = ts[0].tolist().index(True)
		run_analysis(ts, nodes, output_name)
		
def analyze_runs(run_dir, nodes):

	y = [0]*10000
	num_clusters = 0
	clusters = []
	for (root, dirs, files) in os.walk("networks/" + run_dir):
		for dir in dirs:
			input = open(root + "/" + dir + "/user_order.txt", "r")
			user_propogation = json.load(input)
			
			avg = 0
			stream_follow = []
			stream_ts = []
			in_cluster = False
			for ts in user_propogation:
				

				if len(stream_follow) == 50:
					stream_follow.pop(0)
					stream_ts.pop(0)

				stream_ts.append(ts)
				sum_users = sum([len(x) for x in stream_ts])

				sum_followers = sum([nodes[idx][0] for idx in ts])
				stream_follow.append(sum_followers)
				
				
				if sum_users > 200 and not in_cluster:
					cluster = []
					in_cluster = True
					for past_ts in stream_ts:
						for user in past_ts:
							cluster.append(user)
							y[user] = y[user] + 1
					clusters.append(cluster)
				elif sum_users < 200 and in_cluster:
					num_clusters = num_clusters + 1
					in_cluster = False
	
	y2 = [0]*10000
	for idx, count in enumerate(y):
		y2[idx] = nodes[idx][0]

	sorted_degrees = [x for _,x in sorted(zip(y,y2))]
		
	list.sort(y)	
	plt.plot(np.linspace(0,10000,10000),y)
	plt.savefig("networks/10000_1c/200cluster.png")
	plt.show()
	plt.clf()
	
	list.sort(y2)
	plt.plot(np.linspace(0,10000,10000),y2)
	#plt.show()
		
def identify_clusters(run_dir, nodes):
	
	num_clusters = 0
	clusters = []
	for (root, dirs, files) in os.walk("networks/" + run_dir):
		for dir in dirs:
			input = open(root + "/" + dir + "/user_order.txt", "r")
			user_propogation = json.load(input)
			
			
			
if __name__ == "__main__":
	#in degree = num followers
	#out degree = num following
	data_dir = "100000_java"
	
	try:
		os.stat("networks/" + data_dir)
	except:
		os.mkdir("networks/" + data_dir) 
	
	#gen_net(1000, data_dir)
	#nodes = load_network(data_dir)
	#net_analysis(nodes, data_dir)
	run_from_save(data_dir, 1000)
	#analyze_runs(data_dir, nodes)