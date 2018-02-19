import os
import sys
import json
import time
import math
import random
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

from random import choice

def gen_network_graph():
	users = []
	nodes = set()
	graph = nx.DiGraph()

	g = nx.read_weighted_edgelist("networks/10000_1c/edges.csv", nodetype=int, create_using=nx.DiGraph())

	return g
	
def analyze_distance(g):
	input = open("final_clusters.txt", "r")
	clusters = json.load(input)
	
	degrees = []
	for cluster in clusters:
		for i, node_a in enumerate(cluster):
			degrees.append(g.degree(node_a))
			for node_b in cluster[i+1:]:
				print("from " + str(node_a) + " to " + str(node_b) + " path: " + str(nx.shortest_path(g, source=node_a, target=node_b)))
				print(len(nx.shortest_path(g, source=node_a, target=node_b)))	
	

def second_degree(g):
	input = open("final_clusters.txt", "r")
	clusters = json.load(input)
	
	cluster_nodes = []
	for cluster in clusters:
		for i, node in enumerate(cluster):
			cluster_nodes.append(node)	
			
		

	cluster_vals = []
	outside_vals = []
	for node in g:
		followers = g.neighbors(node)
		if len(followers) > 300 and len(followers) < 1000:	
			for s_node in followers:
				out_deg = g.out_degree(s_node)
				if node in cluster_nodes:
					cluster_vals.append(out_deg)
				else:
					outside_vals.append(out_deg)
	

	cluster_vals = sorted(cluster_vals)
	outside_vals = sorted(outside_vals[::3])
	cx = np.linspace(0, len(cluster_vals)-1, len(cluster_vals))
	ox = np.linspace(0, len(outside_vals)-1, len(outside_vals))
	plt.scatter(cx, cluster_vals)
	plt.show()
	plt.clf()
	
	plt.scatter(ox, outside_vals)
	plt.show()
	
def second_deg_indiv(g):
	input = open("final_clusters.txt", "r")
	clusters = json.load(input)
	
	cluster_nodes = []
	for cluster in clusters:
		for i, node in enumerate(cluster):
			cluster_nodes.append(node)	
	
	outside_nodes = []
	for node in g:
		followers = g.neighbors(node)
		if len(followers) > 300 and len(followers) < 1000 and node not in cluster_nodes:	
			outside_nodes.append(node)
	
	sec_rand = random.SystemRandom()
	in_node = sec_rand.choice(cluster_nodes)
	out_node = sec_rand.choice(outside_nodes)
	
	clust_vals = []
	out_vals = []
	for follower in g.neighbors(in_node):
		clust_vals.append(g.out_degree(follower))
		
	for follower in g.neighbors(out_node):
		out_vals.append(g.out_degree(follower))
		
	clust_vals = sorted(clust_vals)
	out_vals = sorted(out_vals)
	cx = np.linspace(0, len(clust_vals)-1, len(clust_vals))
	ox = np.linspace(0, len(out_vals)-1, len(out_vals))

	
	plt.scatter(cx, clust_vals, c='b',s=1)
	plt.scatter(ox, out_vals,c='r', s=1)
	plt.show()
	plt.clf()

if __name__ == "__main__":
	g = gen_network_graph()
	second_deg_indiv(g)