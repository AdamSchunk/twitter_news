import os
import random
import numpy as np
import matplotlib.pyplot as plt

from scipy import optimize

nodes = []
node_edges = []
available_follows = []

def write_node_output(output_file):
	res = "id,num_following\n"
	for node in nodes:
		res = res + ",".join(node)
		
	output = open(output_file, "w")
	
	output.write(res)
	
def  write_edge_output(output_file):
	res = "from,to,weight\n"
	for edge in eges:
		res = res + edge[0] + "," + edge[1]
		
	output = open(output_file, "w")
	
	output.write(res)

def piecewise_linear(x, x0, y0, k1, k2):
    return np.piecewise(x, [x < x0], [lambda x:k1*x + y0-k1*x0, lambda x:k2*x + y0-k2*x0])
	
def deg_func():
	res = 0
	x = [.0031622, .31622, 31.622, 177.8, 562.3] #*10e4 (probability of getting y)
	#-6.75, -4.47, -2.75, -1.75, -1.25
	y = [10000,1000,100,10,1]
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
		node_edges.append([])
		available_follows.append(deg)

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
		if len(node_edges[i]) < nodes[i][1]:
			return True
	return False
		
def gen_edges():
	con_avail = np.full(len(nodes), True)
	while True in con_avail:
		for i, node in enumerate(nodes):
			if con_avail[i] == False:
				continue
			rconn = i
			while rconn == i:
				rconn = random.randint(0,len(nodes))
			node_edges[i].append(rconn)
			con_avail[i] = len(node_edges[i]) < nodes[i][1]
	
if __name__ == "__main__":
	n = 1000
	clustering = .5
	gen_nodes(n)
	gen_edges()
	#write_node_output("networks/test.txt")
	#print(r)