import threading
from UDP_client import UDP_client

class UDP_message_helper(threading.Thread):
    def __init__(self, msg, q):
        super(UDP_message_helper, self).__init__()
        self.message = msg
        self.queue = q
    def run(self):
        self.queue.put(UDP_client.send_message(self.message))