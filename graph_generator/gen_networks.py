import os
import copy
import random
import math
import numpy as np
import matplotlib.pyplot as plt

'''
In my model the arrows point opposite from the paper referenced.
In the paper the A -> B represents A follows B
Here A -> B represents information flows from A to B (B follows A)
'''
def load_network(node_input, edge_input):
	node_file = open(node_input, "r")
	edge_file = open(edge_input, "r")
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
		
	output = open(output_file, "w")
	
	output.write(res)
	
def write_edge_output(nodes, output_file):
	all_edges = []
	res = "from,to,weight\n"

	for i, node in enumerate(nodes):
		for edge in node[1]:
			res = res + str(i) + "," + str(edge) + ",1\n"
		
		
	output = open(output_file, "w")
	
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
	

def clust_func():
	res = 0
	x = [1, 10000] 
	y = [.3,.05]
	r = random.uniform(1, 10000)
	for i, x1 in enumerate(x):
		if r <= x1:
			x_dis = (r-x[i-1])/(x[i]-x[i-1])
			res = int(x_dis*(y[i-1]-y[i]) + y[i])
			break
	return res
			
			
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
		
		mult = 1+len(intersect)/5
		
		weights[i] = weights[i] * mult
		
	return weights
	
#generates edges, adds one follower (out arrow) to each node sequentially until
#no more followers are available in any node
def gen_edges(nodes):
	followers_available = np.full(len(nodes), True)
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
	
def tweet(node_idx, tweeted, seen):
	tweeted[node_idx] = True
	for follower in nodes[node_idx][1]:
		seen[follower] = seen[follower] + 1
	
	
def run_network(nodes):
	tweeted = np.full(len(nodes), False)
	seen = np.full(len(nodes), 0)
	timesteps = []
	rconn = random.randint(0,len(nodes)-1)
	tweet(rconn, tweeted, seen)
	
	count = 0
	while count < 5:
		timesteps.append(copy.deepcopy(tweeted))
		tweet_next = []
		for i in range(0, len(tweeted)):
			if not tweeted[i] and seen[i]:
				r = random.uniform(0,1)
				if r > max(math.pow(.98,seen[i]), .95):
					tweet_next.append(i)
		if not tweet_next:
			count += 1
		else:
			count = 0
			
		for tweeter in tweet_next:
			tweet(tweeter, tweeted, seen)
	return timesteps
			
def gen_net(n, clustering):
	nodes = gen_nodes(n)
	edges = gen_edges(nodes)
	write_node_output(nodes, "networks/NodeTest.csv")
	write_edge_output(nodes, "networks/EdgeTest.csv")
	
def analysis(timesteps, nodes):
	x = np.linspace(0, len(timesteps)-1, len(timesteps), endpoint=True)
	y = []
	
	for ts in timesteps:
		y.append(np.count_nonzero(ts == True))
		
	plt.plot(x,y)
	plt.show()
	#plt.savefig(directory + file_name)
	#plt.clf()
	
def run_from_save(node_file, edge_file):
	nodes = load_network(node_file, edge_file)
	ts = run_network(nodes)
	while np.count_nonzero(ts[-1] == True) <= 5: # if less than 6 people tweeted, redo the analysis
		ts = run_network(nodes)
	analysis(ts, nodes)
			
if __name__ == "__main__":
	#in degree = num followers
	#out degree = num following
	gen_net(1000,.5)
	#run_from_save("networks/NodeTest.csv", "networks/EdgeTest.csv")