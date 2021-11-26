import threading
from UDP_client import UDP_client

class UDP_message_helper(threading.Thread):
    def __init__(self, udp_client, msg, q):
        super(UDP_message_helper, self).__init__()
        self.message = msg
        self.queue = q
        self.udp_client = udp_client
    def run(self):
        self.queue.put(self.udp_client.send_message(self.message))
