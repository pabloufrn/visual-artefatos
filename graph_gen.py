import json
import pandas as pd
import requests_cache
from matplotlib.ticker import MaxNLocator
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
	# Checar token
	access_token = config.get('github_token', '')
	if(not github_util.check_token(config.get('github_token', ''))):
		token_ok = False
		while(not token_ok):
			access_token = input("Token invalido. Cole seu token do github: ")
			token_ok = github_util.check_token(access_token)
		config['github_token'] = access_token
		with open("config.json", "w") as config_file:
			config_file.write(json.dumps(config, sort_keys=True, indent=4))
	requests_cache.install_cache('main_cache', expire_after=None)
	gdao = GDao(config["neo4j"]["host"], config["neo4j"]["port"], config["neo4j"]["user"], config["neo4j"]["pass"])
	return True

def gerar_grafo_issues():
	print("[...] Gerando grafo gerado por issues")
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
			issues += github_util.list_issues(repo, config.get('github_token', ''))
		except StopIteration:
			stop = True
	if(len(issues) == 0):
		print("[!] Não foi possível obter issues. Verifique a existencia de erros nos logs.")
		return
	gdao.save_issues(issues)

def gerar_grafo_pulls():
	print("[...] Gerando grafo gerado por pulls")
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
	# baixar e salvar as pulls
	pulls = []
	page = 0
	stop = False
	while(not stop):
		try:
			repo = next(repo_iter)
			pulls += github_util.list_pulls(repo, config.get('github_token', ''))
		except StopIteration:
			stop = True
	if(len(pulls) == 0):
		print("[!] Não foi possível obter pulls. Verifique a existencia de erros nos logs.")
		return
	gdao.save_pulls(pulls)

def gerar_grafo_commits():
	print("[...] Gerando grafo gerado por commits")
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
	# baixar e salvar as commits
	commits = []
	page = 0
	stop = False
	while(not stop):
		try:
			repo = next(repo_iter)
			commits += github_util.list_commits(repo, config.get('github_token', ''))
		except StopIteration:
			stop = True
	if(len(commits) == 0):
		print("[!] Não foi possível obter commits. Verifique a existencia de erros nos logs.")
		return
	gdao.save_commits(commits)

def resetar_dados():
	print("[...] Resetando dados.")
	if(not carregar_ambiente()):
		print("[!] Arquivo de configuração não definido.")
	else:
		gdao.clear()

def gerar_grafico_issues_part():
	print("[...] Gerando grafico de popularidade das issues")
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
			issues += github_util.list_issues(repo, config.get('github_token', ''))
		except StopIteration:
			stop = True
	if(len(issues) == 0):
		print("[!] Não foi possível obter issues. Verifique a existencia de erros nos logs.")
		return
	# gerar número de eventos para cada issue
	events = {'title': [], 'events': []}
	for issue in issues:
		events['title'].append(f"{issue['number']}. {issue['title']}")
		events['events'].append(github_util.count_events(repo, config.get('github_token', ''), issue['number']))
	# gerar gráfico
	df = pd.DataFrame(data=events)
	dfmax = df.sort_values('events', ascending=False).head(10).sort_values('events')
	dfmin = df.sort_values('events').head(10).sort_values('events', ascending=False)
	gmax = dfmax.plot.barh(x='title', y='events')
	figmax = gmax.get_figure()
	gmax.xaxis.set_major_locator(MaxNLocator(integer=True))
	figmax.savefig('issues_part_max.png', bbox_inches='tight')
	gmin = dfmin.plot.barh(x='title', y='events')
	figmin = gmin.get_figure()
	gmin.xaxis.set_major_locator(MaxNLocator(integer=True))
	figmin.savefig('issues_part_min.png', bbox_inches='tight')

if __name__ == '__main__':
	print("Esse é apenas um módulo, execute o main.py")
