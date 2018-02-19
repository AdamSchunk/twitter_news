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
	y = []
	for i in range(10000):
		y.append([0]*10000)
	
	for (root, dirs, files) in os.walk("networks/10000_1c"):
		for dir in dirs:
			input = open(root + "/" + dir + "/user_order.txt", "r")
			user_propogation = json.load(input)
			ts_window = []
			for i, ts in enumerate(user_propogation):
				ts_window.append(ts)
				if len(ts_window) > 75:
					ts_window.pop(0)
				
				if i < 50 and i > len(user_propogation) - 50:
					continue
				
				for user in ts:
					if nodes[user][0] < 100 or nodes[user][0] > 2000:
						continue
					for slot in ts_window:
						for user_w in slot:
							if nodes[user_w][0] < 100 or nodes[user_w][0] > 2000:
								continue
							y[user][user_w] = y[user][user_w] + 1
					
	
	for i, user_window in enumerate(y):
		for follower in nodes[i][1]:
			user_window[follower] = 0
		
		
	with open('clustering_filtered_by_size.txt', 'w') as outfile:
		outfile.write(json.dumps(y, indent = 4))
	
	
#takes in the windows from every node within range
#returns all the windows with possible clusters in them
def generate_potential_clusters(nodes):
	input = open("clustering_filtered_by_size.txt", "r")
	user_windows = json.load(input)
	
	cluster_candidates = []
	for i, user_window_count in enumerate(user_windows):
		if sum(user_window_count) == 0:
			continue
		array = []
		for node_idx, node_count in enumerate(user_window_count):
			if node_count > 15:
				array.append(node_idx)
		cluster_candidates.append(array)
	
	clusters = []
	for i,a in enumerate(cluster_candidates):
		for b in cluster_candidates[i+1:]:
			overlap = list((set(a) & set(b)))
			if len(overlap) > 10:
				clusters.append(overlap)
	
	print(len(clusters))
	
	with open('potential_clusters.txt', 'w') as outfile:
		outfile.write(json.dumps(clusters, indent = 4))
	
#takes in windows around nodes with possible clusters in them
#returns interesting clusters in the network
def find_clusters(nodes):
	print("finding clusters\n")
	input = open("potential_clusters.txt", "r")
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
	data_dir = "10000_1c"
	
	try:
		os.stat("networks/" + data_dir)
	except:
		os.mkdir("networks/" + data_dir) 
	
	#gen_net(10000, data_dir)
	nodes = load_network(data_dir)
	#net_analysis(nodes, data_dir)
	#run_from_save(data_dir, 1000)
	#generate_windows(data_dir, nodes)
	#generate_potential_clusters(nodes)
	find_clusters(nodes)