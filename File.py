
#   File object contains the name of the file and 
#   the name of the client that holds it

class File(dict):
    def __init__(self, name, clients=None):
        super().__init__()
        if clients is None:
            clients = []
        self['name'] = name
        self['clients'] = clients
