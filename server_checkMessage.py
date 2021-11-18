import threading
import json
from ServerSide import ServerSide
import ast


class ServerCheckMessage(threading.Thread):
    def __init__(self, msg, addr, s):
        super(ServerCheckMessage, self).__init__()
        self.msg = msg
        self.server_host = addr[0]
        self.server_port = addr[1]
        self.s = s
        self.serverSide = ServerSide()
    def run(self):
        print(self.msg)
        msg_dict = ast.literal_eval((self.msg.decode('utf-8')))
        print(msg_dict)
        reply = self.serverSide.get_reply(msg_dict)
        reply_json = json.dumps(reply)

        try:
            self.s.sendto(reply_json.encode(), (self.server_host, self.server_port))
 
        except self.s.error as msg:
            print('Error')
        
        