import requests
import urllib.parse

def list_issues(repo, token):
	no_issues = [["identificador"]]
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
					no = [issue['id']]
					no_issues.append(no)
			else:
				stop = True
		else:
			print("[#] Erro na requisição.")
		page+=1

	return no_issues