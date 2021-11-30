import threading
import json
from ServerSide import ServerSide
import ast

#   Server thread created from UDP_server class, used to 
#   send message to ServerSide and retrieve reply after
#   the command is executed

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
        msg_dict = json.loads(self.msg.decode('utf-8'))
        print(msg_dict)
        print(type(msg_dict))
    

        reply = self.serverSide.get_reply(msg_dict)     #   Parse the message using ServerSide.get_reply()
        reply_json = json.dumps(reply)                  #   Translate the reply to json format

        try:
            self.s.sendto(  reply_json.encode(),        #   Send the json back to the client
                            (self.server_host, 
                            self.server_port))     
 
        except self.s.error as msg:
            print('Error')
        
        