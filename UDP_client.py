import socket
import sys
import json
import traceback

from ClientSide import ClientSide


class UDP_client:
    def __init__(self, client_side, server_host, server_port):
        self.cs = client_side
        self.s = socket
        self.HOST = self.cs.ip
        self.PORT = self.cs.udp_socket
        self.SERVER_HOST = server_host
        self.SERVER_PORT = server_port
        self.ip = self.HOST
        self.tcp = self.cs.tcp_socket
        self.udp = self.PORT
        self.name = self.cs.name

        self.timeout_counter = 3

        self.client_init()
        self.bind_socket()

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
            return self.cs.RETRIEVE_INFOT
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
        except socket.error as msg:
            traceback.print_exc()
            reply = str(msg)
            print("Error: " + str(msg))
    
        return reply

# udp_client = UDP_client(8880)
# udp_client.start()
# udp_client.join()
