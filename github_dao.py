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
			keys = ('id', 'login', 'url', 'html_url')
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
					keys = ('id', 'url', 'login', 'html_url')
					props = {k:issue['milestone']['creator'][k] for k in keys if k in issue['milestone']['creator']}
					nodemc = Node("user", **props)
			# Criar assignees
			nodes_assignees = []
			for assignee in issue['assignees']:
				keys = ('id', 'login', 'url', 'html_url')
				props = {k:assignee[k] for k in keys if k in assignee}
				nodea = Node('user', **props)
				tx.merge(nodea, 'user', 'id')
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
			# Assignees e Issue 
			for nodea in nodes_assignees:
				ai = Relationship(nodea, "PARTICIPA_DE", nodei)
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
	
	def save_pulls(self, pulls):
		self.connect()
		tx = None
		try:
			tx = self.graph.begin()
		except Exception as e:
			print("[!] Não foi possível se conectar a base de dados. Motivo: ")
			print("[-] " + str(e))
			exit()
		for pull in pulls:
			keys = ('id', 'login', 'html_url', 'url')
			props = {k:pull['user'][k] for k in keys if k in pull['user']}
			nodeu = Node("user", **props)
			# Criar labels
			nodes_label = []
			for label in pull['labels']:
				keys = ('id', 'name', 'url', 'default')
				props = {k:label[k] for k in keys if k in label}
				nodel = Node("label", **props)
				tx.merge(nodel, 'label', 'id')
				nodes_label.append(nodel)
			# Criar milestone e criadores
			nodem = None
			nodemc = None
			if(pull['milestone']):
				keys = ('id', 'title', 'url', 'html_url', 'open_issues', 'closed_issues', 'description')
				props = {k:pull['milestone'][k] for k in keys if k in pull['milestone']}
				nodem = Node("milestone", **props)
				tx.merge(nodem, 'milestone', 'id')
				if(pull['milestone']['creator']['id'] == pull['user']['id']):
					nodemc = nodeu
				else: 					
					keys = ('id', 'login', 'html_url', 'url')
					props = {k:pull['milestone']['creator'][k] for k in keys if k in pull['milestone']['creator']}
					nodemc = Node("user", **props)
			# Criar assignees
			nodes_assignees = []
			for assignee in pull['assignees']:
				keys = ('id', 'login', 'html_url', 'url')
				props = {k:assignee[k] for k in keys if k in assignee}
				nodea = Node('user', **props)
				tx.merge(nodea, 'user', 'id')
				nodes_assignees.append(nodea)
			# Criar Reviewers
			nodes_requested_reviewers = []
			for reviewer in pull['requested_reviewers']:
				keys = ('id', 'login', 'html_url', 'url')
				props = {k:reviewer[k] for k in keys if k in reviewer}
				noderv = Node('user', **props)
				tx.merge(noderv, 'user', 'id')
				nodes_requested_reviewers.append(noderv)
			# ToTest: Criar commits
			nodes_commits = []
			for commit in pull['commits']:
				keys = ('sha', 'html_url','url')
				props = {k:commit[k] for k in keys if k in commit}
				props['message'] = commit['commit']['message']
				nodecm = Node('user', **props)
				tx.merge(nodecm, 'commit', 'sha')
				if(commit['author']):
					at = commit['author']
					props['author'] = at['login']
					keys = ('id', 'login', 'html_url', 'url')
					props_at = {k:at[k] for k in keys if k in at}
					nodeat = Node('user', **props_at)
					tx.merge(nodeat, 'user', 'id')
					tx.create(Relationship(nodeat, "É_AUTOR_DE", nodecm))
				if(commit['committer']):
					ct = commit['committer']
					props['committer'] = ct['login']
					keys = ('id', 'login', 'html_url', 'url')
					props_ct = {k:ct[k] for k in keys if k in ct}
					nodect = Node('user', **props_ct)
					tx.merge(nodect, 'user', 'id')
					tx.create(Relationship(nodect, "É_COMMITTER_DE", nodecm))
				nodes_assignees.append(nodecm)
			# TODO: Criar a relação entre commits, criar a relação de pull somente com o primeiro commit
			# deletar atributos não primitivos
			del pull['commits']
			del pull['labels']
			del pull['user']
			del pull['milestone']
			del pull['assignees']
			del pull['requested_reviewers']
			# User e pulls
			nodei = Node("pull", **pull)
			tx.merge(nodeu, "user", "id")
			tx.merge(nodei, "pull", "id")
			ui = Relationship(nodeu, "CRIOU", nodei)
			tx.create(ui)
			# ToTest: Merge and pull
			if('merge_commit_sha' in pull):
				nodemc = Node('merge_commit', sha=pull['merge_commit_sha'])
				tx.merge(nodemc, 'merge_commit', 'sha')
				tx.create(Relationship(nodei, "FOI_MESCLADO_EM", nodemc))
			# Pull e labels
			for nodel in nodes_label:
				il = Relationship(nodei, "ROTULADO_POR", nodel)
				tx.create(il)
			# Assignees e Pull
			for nodea in nodes_assignees:
				ai = Relationship(nodea, "PARTICIPA_DE", nodei)
				tx.create(ai)
			# Milestone e Pulls
			if(nodem):
				mi = Relationship(nodem, "CONTÉM", nodei)
				tx.create(mi)
			# Criador e Milestone
			if(nodemc):
				mmc = Relationship(nodemc, "CRIOU", nodem)
				tx.create(mmc)
			# Revisores e issue
			for noderv in nodes_requested_reviewers:
				rvi = Relationship(noderv, "É_REVISOR_DE", nodei)
				tx.create(rvi)
			# Pull e commits
			for nodecm in nodes_commits:
				tx.create(Relationship(nodei, "CONTÉM", nodecm))
		tx.commit()

	def clear(self):
		self.connect()
		self.graph.delete_all()
		print("[!] Todos os dados foram deletados.")

