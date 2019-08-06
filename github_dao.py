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
			keys = ('id', 'login', 'html_url')
			props = {k:issue['user'][k] for k in keys if k in issue['user']}
			nodeu = Node("user", **props)
			pull_request = False
			if('pull_request' in issue):
				pull_request = True
				del issue['pull_request']
			# Criar labels
			nodes_label = []
			for label in issue['labels']:
				keys = ('id', 'name', 'url', 'default')
				props = {k:label[k] for k in keys if k in label}
				nodel = Node("label", **props)
				tx.merge(nodel, 'label', 'id')
				nodes_label.append(nodel)
			
			# Criar milestone e criadores
			nodem = None
			nodemc = None
			if(issue['milestone']):
				keys = ('id', 'title', 'url', 'html_url', 'open_issues', 'closed_issues', 'description')
				props = {k:issue['milestone'][k] for k in keys if k in issue['milestone']}
				nodem = Node("milestone", **props)
				tx.merge(nodem, 'milestone', 'id')
				if(issue['milestone']['creator']['id'] == issue['user']['id']):
					nodemc = nodeu
				else: 					
					keys = ('id', 'login', 'html_url')
					props = {k:issue['milestone']['creator'][k] for k in keys if k in issue['milestone']['creator']}
					nodemc = Node("user", **props)

			# Criar assignees
			nodes_assignees = []
			for assignee in issue['assignees']:
				keys = ('id', 'login', 'html_url')
				props = {k:assignee[k] for k in keys if k in assignee}
				nodea = None if assignee['id'] == issue['user']['id'] else Node('user', **props)
				nodes_assignees.append(nodea)
			# deletar atributos não primitivos
			del issue['labels']
			del issue['user']
			del issue['milestone']
			del issue['assignees']
			# User e issues
			nodei = Node("pull" if pull_request else "issue", **issue)
			tx.merge(nodeu, "user", "id")
			tx.merge(nodei, "pull" if pull_request else "issue", "id")
			ui = Relationship(nodeu, "CRIOU", nodei)
			tx.create(ui)
			# Issue e labels
			for nodel in nodes_label:
				il = Relationship(nodei, "ROTULADO_POR", nodel)
				tx.create(il)
			# Assihnees e Issue 
			for nodea in nodes_assignees:
				if(nodea == None):
					nodea = nodeu
				ai = Relationship(nodea, "Participa", nodei)
				tx.create(ai)
			# Milestone e issues
			if(nodem):
				mi = Relationship(nodem, "CONTÉM", nodei)
				tx.create(mi)
			# Criador e Milestone
			if(nodemc):
				mmc = Relationship(nodemc, "CRIOU", nodem)
				tx.create(mmc)
		tx.commit()
	
	def clear(self):
		self.connect()
		self.graph.delete_all()
		print("[!] Todos os dados foram deletados.")

