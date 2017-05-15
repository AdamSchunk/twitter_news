import twitter_tools

class user(object):
	
	def __init__(self, username):
		self.screen_name = username
		self.followers = []
		self.following = []
		self.num_followers = 0
		self.num_following = 0