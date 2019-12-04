class InvalidTokenError(Exception):
    def __init__(self, *args,**kwargs):
        Exception.__init__(self,*args,**kwargs)

class InvalidConfigError(Exception):
    def __init__(self, *args,**kwargs):
        self.items = args
        Exception.__init__(self,*args,**kwargs)

class AuthNeo4jError(Exception):
    def __init__(self, *args,**kwargs):
        Exception.__init__(self,*args,**kwargs)
