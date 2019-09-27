import requests
import urllib.parse
import logging

logging.basicConfig(filename='log/requests.log', filemode='w+', format='[%(levelname)s] %(message)s')

def list_issues(repo, token):
	issues = []
	stop = False
	page = 1
	attempt = 0
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
					keys = ('id', 'number', 'title','user','html_url','pull_request','url','labels','milestone','assignees')
					props = {k:issue[k] for k in keys if k in issue}
					issues.append(props)
			else:
				stop = True
		else:
			print("[#] Erro na requisição. Veja a resposta no log.")
			logging.error('url:{} resposta:{}'.format(url, request.text))
			if(attempt >= 2):
				return []
			attempt += 1
		page+=1
	return issues
	
def list_pulls(repo, token):
	pulls = []
	stop = False
	page = 1
	attempt = 0
	while not stop:
		per_page = 100
		params = {
			'state': 'all',
			'page': page,
			'per_page': per_page,
			'access_token': token
		}
		url = 	'https://api.github.com/repos/{}/pulls?'.format(repo)+\
				urllib.parse.urlencode(params)
		print(("[/*] requisitando pulls:"+\
	    	"\n\trepo: {}\n\turl:{}").format(repo, url)+"\n[*/]")
		request = requests.get(url)
		if request.ok:
			conteudo = request.json()
			number_rows = len(conteudo)
			if(number_rows < per_page):
				stop = True
			if(len(conteudo) > 0):
				for pull in conteudo:
					keys = ('id', 'title','user','html_url','url','labels','milestone','assignees', 'requested_reviewers')
					# DOING
					props = {k:pull[k] for k in keys if k in pull}
					# commit: ('sha', 'html_url','url', 'commit','committer','parents')
					props['commits'] = list_commits_pull(repo, token, pull['commits_url'])
					pulls.append(props)
			else:
				stop = True
		else:
			print("[#] Erro na requisição. Veja a resposta no log.")
			logging.error('url:{} resposta:{}'.format(url, request.text))
			if(attempt >= 2):
				return []
			attempt += 1
		page+=1
	return pulls
def list_commits_pull(repo, token, commits_url):
	commits = []
	stop = False
	page = 1
	attempt = 0
	while not stop:
		per_page = 100
		params = {
			'state': 'all',
			'page': page,
			'per_page': per_page,
			'access_token': token
		}
		url = 	commits_url+'?'+\
				urllib.parse.urlencode(params)
		print(("[/*] requisitando commits:"+\
	    	"\n\trepo: {}\n\turl:{}").format(repo, url)+"\n[*/]")
		request = requests.get(url)
		if request.ok:
			conteudo = request.json()
			number_rows = len(conteudo)
			if(number_rows < per_page):
				stop = True
			if(len(conteudo) > 0):
				for commit in conteudo:
					keys = ('sha', 'html_url','url', 'commit','author', 'committer','parents')
					# DOING
					props = {k:commit[k] for k in keys if k in commit}
					commits.append(props)
			else:
				stop = True
		else:
			print("[#] Erro na requisição. Veja a resposta no log.")
			logging.error('url:{} resposta:{}'.format(url, request.text))
			if(attempt >= 2):
				return []
			attempt += 1
		page+=1
	return commits
def list_commits(repo, token):
	commits = []
	stop = False
	page = 1
	attempt = 0
	while not stop:
		per_page = 100
		params = {
			'state': 'all',
			'page': page,
			'per_page': per_page,
			'access_token': token
		}
		url = 	'https://api.github.com/repos/{}/commits?'.format(repo)+\
				urllib.parse.urlencode(params)
		print(("[/*] requisitando commits:"+\
	    	"\n\trepo: {}\n\turl:{}").format(repo, url)+"\n[*/]")
		request = requests.get(url)
		if request.ok:
			conteudo = request.json()
			number_rows = len(conteudo)
			if(number_rows < per_page):
				stop = True
			if(len(conteudo) > 0):
				for commit in conteudo:
					keys = ('sha', 'url', 'html_url', 'author', 'committer', 'commit', 'parents')
					props = {k:commit[k] for k in keys if k in commit}
					commits.append(props)
			else:
				stop = True
		else:
			print("[#] Erro na requisição. Veja a resposta no log.")
			logging.error('url:{} resposta:{}'.format(url, request.text))
			if(attempt >= 2):
				return []
			attempt += 1
		page+=1
	return commits

def count_events(repo, token, issue_id):
	events = []
	stop = False
	page = 1
	attempt = 0
	counter = 0
	while not stop:
		per_page = 100
		params = {
			'state': 'all',
			'page': page,
			'per_page': per_page,
			'access_token': token
		}
		url = 	'https://api.github.com/repos/{}/issues/{}/timeline?'.format(repo, issue_id)+\
				urllib.parse.urlencode(params)
		print(("[/*] requisitando events:"+\
	    	"\n\trepo: {}\n\turl:{}").format(repo, url)+"\n[*/]")
		request = requests.get(url, headers={'Accept': 'application/vnd.github.mockingbird-preview'})
		if request.ok:
			conteudo = request.json()
			number_rows = len(conteudo)
			counter += number_rows
			if(number_rows < per_page):
				stop = True
		else:
			print("[#] Erro na requisição. Veja a resposta no log.")
			logging.error('url:{} resposta:{}'.format(url, request.text))
			if(attempt >= 2):
				return []
			attempt += 1
		page+=1
	return counter