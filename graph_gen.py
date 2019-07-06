import json
from github_dao import GithubDao
import github_api_csv_util as csv_util

config = None
getters = __import__("repository_getters")
# github_dao = GithubDao(host,port,username,password)

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
	no_issues = [["identificador"]]
	page = 0
	stop = False
	while(not stop):
		try:
			repo = next(repo_iter)
			print(csv_util.list_issues(repo, config['github_token']))
		except StopIteration:
			stop = True 

	# todo: acessar DAO

if __name__ == '__main__':
	print("Esse é apenas um módulo, execute o main.py")
