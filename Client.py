#   Used in ServerSide.py to generate client objects
#   and populate requests with appropriate content
#   for command verification and execution

class Client(dict):
    def __init__(self, name, ip, tcp_socket, udp_socket=None, files=None, RQ=None):
        super().__init__()
        if files is None:
            files = []
        self['RQ'] = RQ
        self['name'] = name
        self['ip'] = ip
        self['udp_socket'] = udp_socket
        self['tcp_socket'] = tcp_socket
        self['files'] = files

#   Return a dicionary containing the client's name, ip and tcp socket'
    def get_client_connection(self):
        my_dict = {'name': self['name'],
                   'ip': self['ip'],
                   'tcp_socket': self['tcp_socket']
                   }
        return my_dict

#   Return a dictionary containing client files
    def get_client_data(self):
        my_dict = self.get_client_connection()
        my_dict['files'] = self['files']
        return my_dict

#   Return a client object containing values from dictionary input
    @classmethod
    def from_dict(cls, my_dict):
        params = ['name', 'ip', 'tcp_socket']
        files = None
        if set(params).issubset(set(list(my_dict.keys()))):
            name = my_dict['name']
            ip = my_dict['ip']
            tcp_socket = my_dict['tcp_socket']
        else:
            return None
        if 'files' in my_dict:
            files = my_dict['files']
        if 'udp_socket' in my_dict:
            udp_socket = my_dict['udp_socket']
        return cls(name, ip, tcp_socket, files=files, udp_socket=udp_socket)