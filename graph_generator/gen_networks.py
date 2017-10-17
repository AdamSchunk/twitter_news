import os
import random
import math
import numpy as np
import matplotlib.pyplot as plt

from scipy import optimize

nodes = []
node_followers = []

def load_network(node_input, edge_input):
	node_file = open(node_input, "r")
	edge_file = open(edge_input, "r")
	nodes_str = node_file.readlines()[1:]
	edges_str = edge_file.readlines()[1:]
	
	for node_str in nodes_str:
		id, followers = node_str.split(",")
		nodes.append([int(id), int(followers)])
		
	for n in nodes:
		node_followers.append([])
		
	for edge_str in edges_str:
		node, follower, weight = edge_str.split(",")
		node = int(node)
		follower = int(follower)
		
		node_followers[node].append(follower)
	
	return nodes, node_followers
		
def write_node_output(output_file):
	res = "id,num_following\n"
	for node in nodes:
		res = res + ','.join(str(x) for x in node) + "\n"
		
	output = open(output_file, "w")
	
	output.write(res)
	
def write_edge_output(output_file):
	all_edges = []
	for i, node in enumerate(node_followers):
		for edge in node:
			all_edges.append([i,edge])
	res = "from,to,weight\n"
	for edge in all_edges:
		res = res + ','.join(str(x) for x in edge) + ",1" + "\n"
		
	output = open(output_file, "w")
	
	output.write(res)

def deg_func():
	res = 0
	x = [.0001, .00177, .31622, 10, 177.8, 562.3] #*10e4 (probability of getting y)
	#-8, -6.75, -4.75, -3, -1.75, -1.25
	y = [100000,10000,1000,100,10,1]
	r = random.uniform(.0031623, 562)
	for i, x1 in enumerate(x):
		if r <= x1:
			x_dis = (r-x[i-1])/(x[i]-x[i-1])
			res = int(x_dis*(y[i-1]-y[i]) + y[i])
			break
	return res
	
def gen_nodes(num):
	for i in range(0,num):
		deg = deg_func()
		nodes.append([i,deg])
		node_followers.append([])

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
		
def connections_available():
	for i, node in enumerate(nodes):
		if len(node_followers[i]) < nodes[i][1]:
			return True
	return False
		
def gen_edges():
	con_avail = np.full(len(nodes), True)
	while True in con_avail:
		for i, node in enumerate(nodes):
			if con_avail[i] == False:
				continue
			rconn = i
			while rconn == i or rconn in node_followers[i]:
				rconn = random.randint(0,len(nodes)-1)
			node_followers[i].append(rconn)
			con_avail[i] = len(node_followers[i]) < nodes[i][1]
			if len(node_followers[i]) == len(nodes)-1:
				con_avail[i] = False
	
def tweet(node_idx, tweeted, seen):
	tweeted[node_idx] = True
	for follower in node_followers[node_idx]:
		seen[follower] = seen[follower] + 1
	
	
def test_network():
	tweeted = np.full(len(nodes), False)
	seen = np.full(len(nodes), 0)
	
	print(len(nodes))
	rconn = random.randint(0,len(nodes)-1)
	tweet(rconn, tweeted, seen)
	
	count = 0
	while count < 5:
		print(tweeted)
		tweet_next = []
		for i in range(0, len(tweeted)):
			if not tweeted[i] and seen[i]:
				r = random.uniform(0,1)
				if r > max(math.pow(.98,seen[i]), .9):
					tweet_next.append(i)
		if not tweet_next:
			count += 1
		else:
			count = 0
			
		for tweeter in tweet_next:
			tweet(tweeter, tweeted, seen)
			
def gen_net(n, clustering):
	gen_nodes(n)
	gen_edges()
	write_node_output("networks/NodeTest.csv")
	write_edge_output("networks/EdgeTest.csv")
			
if __name__ == "__main__":
	#gen_net(1000,.5)
	nodes, node_followers = load_network("networks/NodeTest.csv", "networks/EdgeTest.csv")
	test_network()