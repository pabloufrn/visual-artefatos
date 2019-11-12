import json
import github_util
import requests_cache
import requests

config = None
getters = __import__("repository_getters")
token = None
def carregar_ambiente():
	global config
	with open('config.json') as config_file:
		config = json.load(config_file)
	if(config == None):
		print("[!] Arquivo de configuração não definido.")
		return False
	# Checar token
	if(not github_util.check_token(config.get('github_token', ''))):
		access_token = input("Token invalido. Cole seu token do github: ")
		while(not github_util.check_token(access_token)):
			access_token = input("Token invalido. Cole seu token do github: ")
		config['github_token'] = access_token
		with open("config.json", "w") as config_file:
			config_file.write(json.dumps(config, sort_keys=True, indent=4))
	global token
	token = access_token
	requests_cache.install_cache('main_cache', expire_after=None)
	return True

def get_repositories():
	carregar_ambiente()
	requested_getters = config['getters']
	repositories = []
	for requested_getter in requested_getters:
		Getter = getattr(getters, requested_getter["name"])
		repositories += Getter(requested_getter['data']).list()
	return repositories

def ver_historico_arquivo():
	filepath = input("Digite o caminho do arquivo: ")
	print("[...] Gerando  historico de arquivo")
	repos = get_repositories()
	for repo in repos:
		changes = github_util.list_file_history(repo, token, filepath)
		print(f'--------\nrepositório {repo}, mudanças no arquivo {filepath}.\n--------')
		for change in changes:
			print(f"{change['commit']['author']['name']}: {change['commit']['message']}")
