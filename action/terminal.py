from datetime import datetime
import pytz
from util.config import load_config, load_repositories
from util.github import load_api
from helper.exceptions import InvalidTokenError

config, api = None, None

def init(): 
    global api, config
    config = load_config()
    api = load_api(config)

def show_repo_info():
    init()
    repositories = load_repositories(config)
    for repository in repositories:
        print('*'*5 + ' ' + repository + ' ' + '*'*5)
        data = api.get(f"/repos/{repository}").json()
        print(f"Descrição: {data['description'] if data['description'] else 'Nenhuma'}")
        print(f"Privado? {'Sim' if data['private'] else 'Não'}.")
        print(f"Fork? {'Sim' if data['fork'] else 'Não'}.")
        print(f"Projetos? {'Sim' if data['has_projects'] else 'Não'}.")
        print(f"Wiki? {'Sim' if data['has_wiki'] else 'Não'}.")
        print(f"Pages? {'Sim' if data['has_pages'] else 'Não'}.")
        print(f"Estrelas: {data['stargazers_count']}")
        print(f"Inscritos: {data['subscribers_count']}")
        print(f"Issues abertos: {data['open_issues_count']}")
        print(f"Forks: {data['forks']}")
        dt_created_at = datetime.strptime(data['created_at'], '%Y-%m-%dT%H:%M:%SZ')
        timezone_gh = pytz.timezone('Etc/UTC')
        timezone = pytz.timezone('America/Recife')
        dt_created_at = timezone_gh.localize(dt_created_at)
        dt_created_at = dt_created_at.astimezone(timezone)
        print(f"Criado em: {dt_created_at.strftime('%B %d, %Y, %H:%M:%S')}")