import numpy as np

class Network(object):

	def __init__(self):
		self.used = 0
		self.nodes = []
		self.connections = np.zeros((1,1))
		self.followers = []
		self.following = []
		
	def add_users(self, users):
		self.nodes = self.nodes + users
		
	def add_user(self, username, follower, following):
		used += 1
		net_shape = self.connections.shape[0]
		if used >= net_shape[0]:
			tmp = np.zeros((net_shape[0]*2, net_shape[0]*2)) #if we are running out of space double the matrix size

			
n = Network()

print(n.nodes)

n.add_users(["alice", "bob", "charlie"])

print(n.nodes)