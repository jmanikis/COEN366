import json
import socket
import traceback
import time
from ClientSide import ClientSide


class TCP_client:
    def __init__(self, client_side):
        self.cs = client_side
        self.name = self.cs.name
        self.socket = None
        self.HOST = self.cs.ip
        self.LISTENING_PORT = self.cs.tcp_socket  # {port}
        self.UDP = self.cs.udp_socket  # hardcoded
        self.TCP = (self.HOST, self.LISTENING_PORT)

    def __del__(self):
        pass

    def start(self):
        self.createSocket()
        self.bindSocket()
        self.acceptingConnection()

    # ------------------------TCP-------------------------------
    #      PEER COMMUNICATION - Acting Server Side
    # ----------------------------------------------------------
    def createSocket(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        except socket.error as msg:
            print("Socket creation error: " + str(msg))

    # Binding the Socket and listening for connections
    def bindSocket(self):
        try:
            print("Binding the port: " + str(self.LISTENING_PORT))

            # bind socket
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind(("", self.LISTENING_PORT))

            # listen for connections (max 1 bad connections before throwing error)
            # only listen in TCP.
            self.socket.listen(1)

        except socket.error as msg:
            print("Socket binding error: " + str(msg) + "\n" + "Retrying....")
            self.bindSocket()

    # Establish connections with another Client (Socket must be listening)
    def acceptingConnection(self):
        while True:
            try:
                print("waiting for connection")
                conn, address = self.socket.accept()

                # Prevent timeout from happening
                self.socket.setblocking(1)

                print("Connection has been established with IP: " + address[0] + " | Port : " + str(address[1]))
                request = conn.recv(1024)
                request_dict = json.loads(request)

                print(request_dict)
                file_contents = self.cs.parse_reply(request_dict)  # list of dictionaries
                print(file_contents)

                if file_contents[0]['header'] != 'DOWNLOAD-ERROR':
                    for file_dict in file_contents:
                        json_chunk = json.dumps(file_dict)
                        self.sendFile(conn, json_chunk)
                        print(f"Chunk: {json_chunk}")
                        time.sleep(0.1)
                    print("Data Has been transmitted Successfully")
                    conn.close()
                else:
                    print(f"Download Error: {file_contents[0]['reason']}")
            except:
                traceback.print_exc()
                print("Error accepting connections")

    def sendFile(self, conn, chunk_content):
        conn.sendall(bytes(chunk_content, encoding='utf-8'))

    # ------------------------TCP-------------------------------
    #       PEER COMMUNICATION - Acting Client Side
    # ----------------------------------------------------------
    def receivingClient(self, file):
        rSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        file_name = file
        try:
            clientList = self.cs.get_client_from_file_name(file_name)
            print(f"Client: {clientList} \n")
            if clientList is not None:
                for n in clientList:
                    try:
                        rSocket.connect((clientList[n]['ip'], clientList[n]['tcp_socket']))
                        # rSocket.connect(('localhost', client['tcp_socket']))
                        print(f"Connected to : {clientList[n]['tcp_socket']}")
                        break
                    except:
                        print(f"Cannot connect to client, moving on to next client {n}")
                        continue

                request_dict = self.cs.DOWNLOAD(file_name)
                print(f"Request_dict: {request_dict} \n")
                json_request_dict = json.dumps(request_dict)
                print(f"JSON_Request_dict: {json_request_dict} \n")
                rSocket.sendall(bytes(json_request_dict, encoding='utf-8'))
                print("Data Has been transmitted Successfully")

                # RECEIVE DATA
                while True:
                    received = rSocket.recv(1024)
                    data = json.loads(received)
                    self.cs.parse_reply(data)  # Send json to database and loop to get all dictionaries to database.
                    if data['header'] == "FILE-END":
                        break
                return "File downloaded."
            else:
                print("No Clients Have The Requested File.")
        except:
            traceback.print_exc()
            print("Error Retrieving Client")


