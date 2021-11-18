import threading
import sys
import json


class ServerCheckMessage(threading.Thread):
    def __init__(self, msg, addr, s):
        super(ServerCheckMessage, self).__init__()
        self.msg = msg
        self.server_host = addr(0)
        self.server_port = addr(1)
        self.s = s
    #def run(self):
        #reply = message_helper.MessageHelper.checkMessageType(self.msg)
        
        #msg_json = json.dumps(reply)
        
        #
        #try:
        #    s.sendto(msg_json, (self.server_host, self.server_port))
 
        #except s.error as msg:
        #    print('Error')
        
        