import py2neo

class GithubDao:
	def __init__(self,host,port,username,password):
		self.host = host
		self.port = port
		self.username = username
		self.password = password
	def connect(self):
		pass
	def save_commit(self):
		pass