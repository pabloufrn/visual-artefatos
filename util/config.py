import os
import json
import requests
from helper.exceptions import InvalidConfigError, InvalidTokenError
from util.github import validate_token
from util.neo4j import check_connection

def load_config():

    # Carregar configuração global

	config = {}
	config_changed = False
	try:
		with open('config/global.json') as config_file:
			config = json.load(config_file)
	except:
		pass

	if(config  == {}):
		config_changed = True
		repo = input("Digite o repositório que você quer extrair os dados\n: ")
		config = {"getters": [{"data": [repo], "name": "ListGetter"}]}

	# Validar conexão neo4j
	addr, port, user, dbpw = "localhost" , "7687", "neo4j", "neo4j" 
	if("neo4j" in config):
		addr = config["neo4j"]["addr"] if "addr" in config["neo4j"] else ""
		port = config["neo4j"]["port"] if "port" in config["neo4j"] else ""
		user = config["neo4j"]["user"] if "user" in config["neo4j"] else ""
		dbpw = config["neo4j"]["dbpw"] if "dbpw" in config["neo4j"] else ""
	else: 
		config_changed = True
	result = check_connection(addr, port, user, dbpw)
	while( result == -1):
		print("Endereço para o neo4j inválido ou serviço não foi inicializado.")
		addr = input("Endereço (localhost): ")
		port = input("Porta (7687): ")
		if( port == ""): port = "7687"
		if( addr == ""): addr = "localhost"
		result = check_connection(addr, port, user, dbpw)
	while( result == 1):
		config_changed = True
		print("Erro ao se autentificar com o neo4j, digite suas credenciais novamente.")
		user = input("Usuário: ")
		dbpw = input("Senha: ")
		result = check_connection(addr, port, user, dbpw)

	config["neo4j"] = {"addr": addr, "port": port, "user": user, "dbpw": dbpw}

	# Salvar configuração

	if(config_changed):
		with open("config/global.json", "w+") as config_file:
			config_file.write(json.dumps(config, indent=4))

	# Validar token

	token_changed = False
	access_token = None
	token_file = None
	
	try:
		token_file = open('config/.token')
		access_token = token_file.readline().rstrip('\n')
		token_file.close()
	except:
		pass
	
	while(not validate_token(access_token)):
		token_changed = True
		access_token = input("Digite um token válido\n: ")
	config["access_token"] = access_token

	# Salvar token

	if(token_changed):
		with open("config/.token", "w+") as token_file:
			token_file.write(access_token)

	# Outras operações

	return config

def check_token(token):
	access_token = token
	url = f"https://api.github.com/?access_token={access_token}"
	request = requests.get(url)
	if(request.status_code == 401):
		return False
	elif(request.status_code == 200):
		return True
	else:
		print("Erro: falha na requisição para a api. Tente novamente.")
		exit(1)

def load_repositories(config):
	getters = __import__("repository_getters")
	repositories = []
	for getter in config["getters"]:
		Getter = getattr(getters, getter["name"])
		repositories += Getter(getter['data']).list()
	return repositories