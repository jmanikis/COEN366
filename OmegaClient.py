from UDP_client import UDP_client
from TCP_client import TCP_client
import socket


class OmegaClient:
    def __init__(self):
        self.HOSTNAME = socket.gethostname()
        self.HOST = socket.gethostbyname(self.HOSTNAME)
        self.UDP_port = 9001
        self.TCP_port = 9091
        self.TCP_client = TCP_client()
        self.UDP_Client = UDP_client()
