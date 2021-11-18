import socket
import sys
import threading
import json


class UDP_client(threading.Thread):
    def __init__(self, port):
        super(UDP_client, self).__init__()
        self.s = socket 
        self.HOSTNAME = self.s.gethostname()
        self.HOST = '0.0.0.0'    
        self.PORT = port 
        self.SERVER_HOST = 'localhost'
        self.SERVER_PORT = 8890
    def run(self):
        self.client_init()
        self.bind_socket()
        self.send_message()


    def client_init(self):
        try:
            self.s = self.s.socket(socket.AF_INET, socket.SOCK_DGRAM)
        except socket.error:
            print("Failed to create socket")
            sys.exit()
        
    def bind_socket(self):
        self.s.bind((self.HOST, self.PORT))

    def send_message(self):
        while(1):
            msg_header = input("Enter header to send: ")
            msg_RQ = input("RQ: ")
            msg_name = input("Name: ")
            msg_ip = self.HOST
            msg_tcp = 8881
            msg_udp = self.PORT

            msg_json = json.dumps({"header" : msg_header, "RQ": msg_RQ, "name": msg_name,
            "ip": msg_ip, "tcp_socket":msg_tcp, "udp_socket":msg_udp, "files": ["file1.txt", "file2.txt"]})
            msg_encoded = msg_json.encode()

            try:
                print("UDP_client host: " + str(self.HOST))
                print("UDP_client port: " + str(self.PORT))
                self.s.sendto(msg_encoded, (self.SERVER_HOST, self.SERVER_PORT))

                print("DATA SENT")
                d = self.s.recvfrom(1024)
                reply = d[0]
                addr = d[1]

                # TODO: If not acknowledged, send it again

                print("Server reply: " + reply.decode())
                print("Server addr: " + str(addr[0]) + " " + str(addr[1]))
            except socket.error as msg:
                print("Error " + str(msg))

udp_client = UDP_client(8880)
udp_client.start()
udp_client.join()