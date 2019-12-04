class APIService:

    def __init__( self, base_url):
        self.base_url = base_url
        self.default_get_params = {}

    def do_get( self):
