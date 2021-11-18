class File(dict):
    def __init__(self, name, clients=None):
        super().__init__()
        if clients is None:
            clients = []
        self['name'] = name
        self['clients'] = clients
