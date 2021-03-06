import threading

#   Run a thread to start listening for TCP connection requests
#   from other clients

class TCP_acceptingConnection(threading.Thread):
    def __init__(self, tcp_client):
        super(TCP_acceptingConnection, self).__init__()
        self.tcp_client = tcp_client
    def run(self):
        self.tcp_client.start()

