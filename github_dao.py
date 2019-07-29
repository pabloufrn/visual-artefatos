from py2neo import Graph, Node, Relationship

class GithubDao:
	def __init__(self,host,port,username,password):
		self.host = host
		self.port = port
		self.username = username
		self.password = password
		self.connected = False
	def set_schema(self):
		try:
			self.graph.schema.create_uniqueness_constraint('issue', 'id')
		except Exception as e:
			print("[!] Não foi possível se conectar a base de dados. Motivo: ")
			print("[-] " + str(e))
			exit()
	def connect(self):
		if(self.connected):
			return
		print("[...] Carregandos dados de autenticação da base de dados.")
		self.graph = Graph(host=self.host, port=self.port, 
			user=self.username, password=self.password)
		self.connected = True
		print("[!] Dados de autenticação armazenados.")
		self.set_schema()
	def save_issues(self, issues):
		self.connect()
		tx = None
		try:
			tx = self.graph.begin()
		except Exception as e:
			print("[!] Não foi possível se conectar a base de dados. Motivo: ")
			print("[-] " + str(e))
			exit()
		for issue in issues:
			nodeu = Node("user", login=issue['user']['login'])
			del issue['user']
			nodei = Node("issue", **issue)
			tx.merge(nodeu, "user", "login")
			tx.merge(nodei, "issue", "id")
			ui = Relationship(nodeu, "CRIOU", nodei)
			tx.create(ui)
		tx.commit()
	def clear(self):
		self.connect()
		self.graph.delete_all()
		print("[!] Todos os dados foram deletados.")

