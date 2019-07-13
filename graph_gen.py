import json
from github_dao import GithubDao as GDao
import github_util

config = None
getters = __import__("repository_getters")
# github_dao = GithubDao(host,port,username,password)
gdao = GDao("localhost", "7474", "neo4j", "rootpass")

def carregar_ambiente():
	with open('config.json') as config_file:  
		global config
		config = json.load(config_file)
	if(config == None):
		return False
	return True

def gerar_grafo_completo():
	print("[...] Gerando grafo completo")
	if(not carregar_ambiente()):
		print("[!] Arquivo de configuração não definido.")
		# todo: assistente de configuração
	Getter = getattr(getters, config['repositories']['getter'])
	repo_iter = iter(Getter(config['repositories']['data']))

	# baixar e salvar as issues
	issues = []
	page = 0
	stop = False
	while(not stop):
		try:
			repo = next(repo_iter)
			issues = github_util.list_issues(repo, config['github_token'])
		except StopIteration:
			stop = True 
			
	gdao.save_issues(issues)
	
def resetar_dados():
	gdao.clear()

if __name__ == '__main__':
	print("Esse é apenas um módulo, execute o main.py")
