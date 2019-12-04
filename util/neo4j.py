from py2neo import Database, Graph
from neobolt.exceptions import AuthError, ServiceUnavailable

def check_connection(addr, port, user, dbpw):
    try:
        Database(f"bolt://{addr}:{port}", auth = (user, dbpw)).kernel_version
    except ServiceUnavailable:
        return -1
    except (AuthError, AttributeError):
        return 1
    return 0

def load_db(config):
    graph = Graph(
        host=config["addr"], port=config["port"], 
		user=config["user"], password=config["dbpw"])
    graph.schema.create_uniqueness_constraint('issue', 'id')
    return graph
