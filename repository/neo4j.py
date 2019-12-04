from py2neo import Graph, Node, Relationship


''' 
### todo:
- testar a conexão
- passar um dicionario
### tothink:
- definir um logger no lugar do print

'''
class Neo4jRepository:

    def __init__( self, host, port, username, password):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.connected = False

    def connect( self):
        if (self.connected): return
        print("[...] Carregandos dados de autenticação da base de dados.")
        self.graph = Graph(host=self.host, port=self.port, 
            user=self.username, password=self.password)
        self.connected = True
        print("[!] Dados de autenticação armazenados.")
