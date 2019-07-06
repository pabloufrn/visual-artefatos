class ListGetter:
	def __init__(self, data):
		self.data = data
	def __iter__(self):
		return iter(self.data)
	def list(self):
		return self.data
	

