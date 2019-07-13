import requests
import urllib.parse

def list_issues(repo, token):
	issues = []
	stop = False
	page = 1
	while not stop:
		per_page = 100
		params = {
			'state': 'all',
			'page': page,
			'per_page': per_page,
			'access_token': token
		}
		url = 	'https://api.github.com/repos/{}/issues?'.format(repo)+\
				urllib.parse.urlencode(params)
		print(("[/*] requisitando issues:"+\
	    	"\n\trepo: {}\n\turl:{}").format(repo, url)+"\n[*/]")
		request = requests.get(url)
		if request.ok:
			conteudo = request.json()
			number_rows = len(conteudo)
			if(number_rows < per_page):
				stop = True
			if(len(conteudo) > 0):
				for issue in conteudo:
					keys = ('id', 'title', 'user')
					props = {k:issue[k] for k in keys if k in issue}
					issues.append(props)
			else:
				stop = True
		else:
			print("[#] Erro na requisição.")
		page+=1
	return issues