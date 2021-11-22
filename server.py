#import registered_users
import socket
import threading
import sys
import server_checkMessage


class UDP_server(threading.Thread):
    def __init__(self, port):
        super(UDP_server, self).__init__()
        self.s = socket
        self.HOST = '0.0.0.0'
        self.PORT = port
        
    def run(self):
        print(self.HOST)
        self.initServer()
        self.listening()

    def initServer(self):
        self.createSocket()
        self.bindSocket()
        
    def listening(self):
        while 1:
            d = self.s.recvfrom(1024)
            data = d[0]
            addr = d[1]
            
            if not data:
                break

            self.startHelper(data, addr, self.s)
            
    
    def startHelper(self, data, addr, s):
        #   
        #   Start a new thread to check deal with the message
        #

        helper = server_checkMessage.ServerCheckMessage(data, addr, s)
        helper.start()
        helper.join()


    def createSocket(self):
        #
        #   Create a socket to bind to 
        #   

        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            print('Socket Created')
        except socket.error as msg:
            print ('Failed to create socket. Error Code: ') + \
                str(msg[0])\
                + ' Message ' + msg[1]
            sys.exit()

    def bindSocket(self):
        #
        #   Bind the socket
        #

        try:
            self.s.bind((self.HOST, self.PORT))
        except socket.error as msg:
            print ('Bind failed. Error Code: ') + str(msg[0])\
                 + ' Message ' + msg[1]
            sys.exit()

        print ('Socket bind complete')


udp_server = UDP_server(8891)
udp_server.start()
udp_server.join()