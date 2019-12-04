from util.config import load_config, load_repositories
from util.github import load_api
from util.neo4j import load_db
from repository.issue import IssueRepository
from repository.pull import PullRepository
import json

config, api, db = None, None, None

def init(): 
    global api, config, db
    config = load_config()
    api = load_api(config)
    db = load_db(config["neo4j"])

def issues():
    print("[...] Gerando grafo gerado por issues")
    init()
    issue_repository = IssueRepository(db)
    repositories = load_repositories(config)
    issues = []
    for repository in repositories:
        print(f"[...] Obtendo dados de {repository}")
        data = api.get(f"/repos/{repository}/issues", params={"per_page": 100}).json()
        page = 2
        while(len(data) == 100):
            issues += data
            print(f"[!] {100*(page-2)+len(data)} issues carregados.")
            data = api.get(f"/repos/{repository}/issues", params={
                "per_page": 100, "page": page
            }).json()
            page += 1
        issues += data
        print(f"[!] Total de {100*(page-1)+len(data)} obtidos.")
        print(f"[!] Dados de {repository} carregados.")
    print("[...] Salvando na base de dados")
    for issue in issues:
        issue_repository.save(issue)
    print("[!] Salvo")

def pulls():
    init()
    pull_repository = PullRepository(db)
    repositories = load_repositories(config)
    pulls = []
    for repository in repositories:
        pulls += api.get(f"/repos/{repository}/pulls").json()
    for pull in pulls:
        pull_repository.save(pull)