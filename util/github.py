import requests
from util.api import API

def validate_token(token):
	if(token == "" or token == None):
		return False
	url = f"https://api.github.com/?access_token={token}"
	request = requests.get(url)
	if(request.status_code == 401):
		return False
	elif(request.status_code == 200):
		return True
	else:
		raise RuntimeError("Não foi possível fazer a requisição.")

def validate_repo(repo):
	url = f"https://api.github.com/repos/{repo}"
	request = requests.get(url)
	if(request.status_code == 404):
		return False
	elif(request.status_code == 200):
		return True
	else:
		raise RuntimeError("Não foi possível fazer a requisição.")

def load_api(config):
	api = API("https://api.github.com")
	api.default_params = {"access_token": config["access_token"]}
	api.default_headers = {
        'content-type': 'application/json', 
        'Time-Zone': 'Etc/UTC'}
	return api

def filter_props(artifact):
	return {
		k:artifact[k] for k in artifact if 
			type(artifact[k]) != dict and 
			type(artifact[k]) != list and 
			artifact[k] != "" and 
			not k.endswith("url") and
			not k == "node_id"
	}