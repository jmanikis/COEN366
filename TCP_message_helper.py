import threading
from TCP_client import TCP_client

class TCP_message_helper(threading.Thread):
    def __init__(self, tcp_client, input, q):
        super(TCP_message_helper, self).__init__()
        self.message = input
        self.queue = q
        self.tcp_client = tcp_client
    def run(self):
        self.queue.put(self.tcp_client.receivingClient(self.message))
