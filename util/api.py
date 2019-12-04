import requests
import requests_cache

class API: 

    def __init__( self, base_url):
        session = requests.Session()
        github_adapter = requests.adapters.HTTPAdapter(max_retries=10)
        session.mount(base_url, github_adapter)
        self.session = session
        self.base_url = base_url
        self.default_params = {}
        self.default_headers = {}
        requests_cache.install_cache(f"cache/{self.base_url.split('/')[2]}", expire_after=None)

    def get( self, path, *args, **kargs):
        headers = self.default_headers
        params = self.default_params
        if("headers" in kargs): 
            headers.update(kargs)
            del kargs["headers"]
        if("params" in kargs): 
            params.update(kargs["params"])
            del kargs["params"]
        
        return self.session.get(f"{self.base_url}{path}",
            params = self.default_params,
            headers = self.default_headers, *args, **kargs)
    
