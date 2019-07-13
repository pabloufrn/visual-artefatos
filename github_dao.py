from py2neo import Graph, Node, Relationship

class GithubDao:
	def __init__(self,host,port,username,password):
		self.host = host
		self.port = port
		self.username = username
		self.password = password
		self.connected = False
	def connect(self):
		if(self.connected):
			return
		print("[...] Conectando base de dados")
		self.graph = Graph(password="rootpass")
		self.connected = True
		print("[!] Base de dados conectada.")
	def save_issues(self, issues):
		self.connect()
		tx = self.graph.begin()
		for issue in issues:
			nodeu = Node("user", name=issue['user']['login'])
			del issue['user']
			nodei = Node("issue", **issue)
			tx.create(nodeu)
			tx.create(nodei)
			ui = Relationship(nodeu, "CRIOU", nodei)
			tx.create(ui)
		tx.commit()
	def clear(self):
		self.connect()
		self.graph.delete_all()
		print("[!] Todos os dados foram deletados.")

