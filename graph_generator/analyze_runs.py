import os
import json

import numpy as np

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
	
	
def generate_windows(data_dir, nodes):
	print("generating windows")
	final = []
	for node_id, node in enumerate(nodes):
		y = [0]*len(nodes)
		
		if node[0] < 100 or node[0] > 2000:
			continue
		for (root, dirs, files) in os.walk("networks/" + data_dir):
			for dir in dirs:
				input = open(root + "/" + dir + "/user_order.txt", "r")
				user_propogation = json.load(input)
				ts_window = []
				for i, ts in enumerate(user_propogation): #establish the window
					if node_id in ts:
						ts_window = user_propogation[i-30:i+30]

						for slot in ts_window: #for each previous ts in the ts window
							for user_w in slot: #compare against every other user in each ts
								if nodes[user_w][0] < 100 or nodes[user_w][0] > 2000:
									continue
								y[user_w] = y[user_w] + 1
						break
		
		potential_cluster = generate_potential_clusters(y, nodes, node_id)
		final.append(potential_cluster)
		
		
	with open(data_dir + '/potential_clusters.txt', 'w') as outfile:
		outfile.write(json.dumps(final, indent = 4))
	
	
#takes in the windows from every node within range
#returns all the windows with possible clusters in them
def generate_potential_clusters(node_pairings, nodes, node_id):	

	array = []
	for node_idx, node_count in enumerate(node_pairings): #
		if node_count > 15: # and node_idx not in nodes[node_id][1]:
			array.append(node_idx)
		
	print(len(array))
	
	if len(array) == 0:
		print(node_pairings)
	
	return array
	
#takes in windows around nodes with possible clusters in them
#returns interesting clusters in the network
def find_clusters(data_dir, nodes):
	print("finding clusters\n")
	input = open(data_dir + "/potential_clusters.txt", "r")
	potential_clusters = json.load(input)

	num_seen = []
	clusters = []
	cluster_count = []
	for node_window in potential_clusters:
		found = False
		for num_cluster,cluster in enumerate(clusters):
			overlap = list((set(node_window) & set(cluster)))
			if len(overlap) > 5:
				found = True
				clusters[num_cluster] = list(set(cluster + node_window))
				num_seen[num_cluster] = num_seen[num_cluster] + 1
				for node in node_window:
					cc = cluster_count[num_cluster]
					keys = cc.keys()
					if node in keys:
						cc[node] = cc[node] + 1
					else:
						cc[node] = 0
						
					cluster_count[num_cluster] = cc
				
		if not found:
			clusters.append(node_window)
			num_seen.append(0)
			cluster_count.append(dict())
			for node in node_window:
				cluster_count[-1][node] = 0
	
	final_cut = []
	for i, c in enumerate(clusters):
		tmp = []
		if num_seen[i] == 0:
			continue
		for node in c:
			if cluster_count[i][node] > 2:
				tmp.append(node)
		if len(tmp) > 0:		
			final_cut.append(tmp)
				
	with open('final_clusters.txt', 'w') as outfile:
		outfile.write(json.dumps(final_cut, indent = 4))
	
if __name__ == "__main__":
	#in degree = num followers
	#out degree = num following
	data_dir = "100000_java"
	
	try:
		os.stat("networks/" + data_dir)
	except:
		os.mkdir("networks/" + data_dir) 
	
	nodes = load_network(data_dir)
	generate_windows(data_dir, nodes)
	generate_potential_clusters(data_dir, nodes)
	find_clusters(nodes)