from api import APIService as api

'''todo:
- usar asyncio
'''

class GithubService:
    def __init__(base_ufr):
    def validate_token(token):
        api.get("", on_result)
        access_token = token
        token_ok = False
        url = f"https://api.github.com/?access_token={access_token}"
        request = requests.get(url)
        if(request.status_code == 401):
            return False
        elif(request.status_code == 200):
            return True
        else:
            print("Erro: falha na requisição para a api. Tente novamente.")
            exit(1)