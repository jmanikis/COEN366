import socket
import sys
import threading
import json
from ClientSide import ClientSide


class UDP_client(threading.Thread):
    def __init__(self, port):
        super(UDP_client, self).__init__()
        self.s = socket 
        self.HOSTNAME = self.s.gethostname()
        self.HOST = '0.0.0.0'    
        self.PORT = port 
        self.SERVER_HOST = 'localhost'
        self.SERVER_PORT = 8891
        self.currentRQ = 0
        self.nextRQ = 1
        self.ip = "0.1.0.1"
        self.tcp = 8881
        self.udp = 8882
        self.name = None
        self.cs = None
    def run(self):
        self.client_init()
        self.bind_socket()
        self.client_side_init()
        self.send_message()


    def client_init(self):
        try:
            self.s = self.s.socket(socket.AF_INET, socket.SOCK_DGRAM)
        except socket.error:
            print("Failed to create socket")
            sys.exit()
        
    def bind_socket(self):
        self.s.bind((self.HOST, self.PORT))

    def client_side_init(self):
        self.name = input("Please enter your name: ")
        self.cs = ClientSide(self.name, self.ip, self.udp, self.tcp)

    #   used in loop to choose request command to send to server.
    def send_helper(self):
        choices = [ "1.  REGISTER", "2.  RE-REGISTER",  "3.  PUBLISH",
                    "4.  REMOVE", "5.  RETRIEVE-ALL", "6.  SEARCH-FILE",
                    "7.  RETRIEVE-INFOT","8.  UPDATE-CONTACT", 
                    "9.  DOWNLOAD"]
        for c in choices:
            print(c)
        choice = input("Please enter the index of your choice: ")
        return self.message_builder(choice)

    #   send_helper calls this method.
    def message_builder(self, choice):
        if choice == '1':
            return self.cs.REGISTER()
        elif choice == '2':
            return self.cs.DE_REGISTER()
        elif choice == '3':
            files = []
            while True:
                file = input("Please enter list of files to publish as a dict: ")
                if ".txt" in file:
                    files.append(file)
                else:
                    break
            return self.cs.PUBLISH(files)
        elif choice == '4': 
            files = input("Please enter list of files to remove as a dict: ")
            return self.cs.REMOVE(files)
        elif choice == '5':
            return self.cs.RETRIEVE_ALL()
        elif choice == '6':
            file = input("Please enter file to search: ")
            return self.cs.SEARCH_FILE(file)
        elif choice == '7':
            name = input("Please enter the name of the person desired: ")
            return self.cs.RETRIEVE_INFOT(name)
        elif choice == '8':
            return self.cs.UPDATE_CONTACT()
        elif choice == '9': 
            dl = input("Please enter the name of the file you would like to download: ")
            return self.cs.DOWNLOAD(dl)
        else:
            choice = input("Please use one of the indexes, and try again: ")
            return self.message_builder(choice)

    def send_message(self):
        while(1):

            msg = self.send_helper()

            msg_json_cs = json.dumps(msg)
            msg_encoded = msg_json_cs.encode()

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