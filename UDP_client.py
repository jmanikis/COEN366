import socket
import sys
import threading
import json
from ClientSide import ClientSide
import select


class UDP_client(threading.Thread):
    def __init__(self, name, UDP_port, TCP_port, host, server_host, server_port):
        super(UDP_client, self).__init__()
        self.s = socket
        # self.HOSTNAME = self.s.gethostname()
        # self.HOST = self.s.gethostbyname(self.HOSTNAME)
        self.HOST = host
        self.PORT = UDP_port
        self.SERVER_HOST = server_host
        self.SERVER_PORT = server_port
        self.currentRQ = 0
        self.nextRQ = 1
        self.ip = self.HOST
        self.tcp = TCP_port
        self.udp = self.PORT
        self.name = name
        self.cs = ClientSide(self.name, self.HOST, self.udp, self.tcp)
        self.timeout_counter = 3

        self.client_init()
        self.bind_socket()

    def run(self):
        self.client_init()
        self.bind_socket()
        self.client_side_init()
        self.send_message()

    def client_init(self):
        try:
            self.s = self.s.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.s.settimeout(5)
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
        choices = ["1.  REGISTER", "2.  RE-REGISTER", "3.  PUBLISH",
                   "4.  REMOVE", "5.  RETRIEVE-ALL", "6.  SEARCH-FILE",
                   "7.  RETRIEVE-INFOT", "8.  UPDATE-CONTACT",
                   "9.  DOWNLOAD"]
        for c in choices:
            print(c)
        choice = input("Please enter the index of your choice: ")
        return self.message_builder(choice)

    #   send_helper calls this method.
    def message_builder(self, choice, arg=None):
        if choice == '1':
            return self.cs.REGISTER()
        elif choice == '2':
            return self.cs.DE_REGISTER()
        elif choice == '3':
            return self.cs.PUBLISH(arg)
        elif choice == '4':
            return self.cs.REMOVE(arg)
        elif choice == '5':
            return self.cs.RETRIEVE_ALL()
        elif choice == '6':
            return self.cs.SEARCH_FILE(arg)
        elif choice == '7':
            return self.cs.RETRIEVE_INFOT(arg)
        elif choice == '8':
            return self.cs.UPDATE_CONTACT()
        elif choice == 'q':
            return None
        else:
            choice = input("Please use one of the indexes, and try again: ")
            return self.message_builder(choice)

    def send_message(self, msg=None):
            # msg = self.send_helper()
        if msg is None:
            reply = "Message is NONE"
        
        msg_json_cs = json.dumps(msg)
        msg_encoded = msg_json_cs.encode()

        try:
            print("UDP_client host: " + str(self.HOST))
            print("UDP_client port: " + str(self.PORT))
            

            print(msg_encoded)
            print(type(msg_encoded))
            print(self.SERVER_HOST)
            print(self.SERVER_PORT)
            self.s.sendto(msg_encoded, (self.SERVER_HOST, self.SERVER_PORT))

            print("DATA SENT")

            while(self.timeout_counter > 0):
                try: 
                    d = self.s.recvfrom(4096)
                    reply = d[0]
                    addr = d[1]
                    self.timeout_counter = 3
                    break
                except Exception as err:
                    self.timeout_counter = self.timeout_counter - 1
                    print("Timed out - retrying...", err)
            
            if(self.timeout_counter == 0):
                reply = "Time-out 3 times, server not responding."
                self.timeout_counter = 3
            else:
                print("Server reply: " + reply.decode())
                print("Server addr: " + str(addr[0]) + " " + str(addr[1]))
                reply = json.loads(reply.decode())
                self.cs.parse_reply(reply)
                

            # TODO: If not acknowledged, send it again
            # TODO: json.loads reply as dict and pass to self.cs.parse_reply(reply)
            # TODO: return self.cs.parse_reply(reply)
        except socket.error as msg:
            print("Error " + str(msg))
    
        return reply

# udp_client = UDP_client(8880)
# udp_client.start()
# udp_client.join()
