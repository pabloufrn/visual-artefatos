import json
from github_dao import GithubDao as GDao
import github_util

config = None
getters = __import__("repository_getters")
gdao = None

def carregar_ambiente():
	global config, gdao
	with open('config.json') as config_file:  
		config = json.load(config_file)
	if(config == None):
		return False
	gdao = GDao(config["neo4j"]["host"], config["neo4j"]["port"], config["neo4j"]["user"], config["neo4j"]["pass"])
	return True

def gerar_grafo_completo():
	print("[...] Gerando grafo completo")
	if(not carregar_ambiente()):
		print("[!] Arquivo de configuração não definido.")
		# todo: assistente de configuração

	# Carregar todos os repositórios
	requested_getters = config['getters']
	repositories = []
	for requested_getter in requested_getters:
		Getter = getattr(getters, requested_getter["name"])
		repositories += Getter(requested_getter['data']).list()
	repo_iter = iter(repositories)
	# baixar e salvar as issues
	issues = []
	page = 0
	stop = False
	while(not stop):
		try:
			repo = next(repo_iter)
			issues += github_util.list_issues(repo, config['github_token'])
		except StopIteration:
			stop = True 
	if(len(issues) == 0):
		print("[!] Não foi possível obter issues. Verifique a existencia de erros no logs.")
		return
	gdao.save_issues(issues)
	
def resetar_dados():
	print("[...] Resetando dados.")
	if(not carregar_ambiente()):
		print("[!] Arquivo de configuração não definido.")
	else:
		gdao.clear()
		
if __name__ == '__main__':
	print("Esse é apenas um módulo, execute o main.py")
