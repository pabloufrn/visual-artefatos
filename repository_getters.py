class ListGetter:
	def __init__(self, data):
		self.data = data
	def __iter__(self):
		return iter(self.data)
	def list(self):
		return self.data
	
class TxtGetter:
	def __init__(self, data):
		self.data = []
		for txtfile in data:
			with open(txtfile, 'r') as f:
				lines = f.read().splitlines()
				for line in lines:
					self.data.append(line)
	def __iter__(self):
		return iter(self.data)
	def list(self):
		return self.data