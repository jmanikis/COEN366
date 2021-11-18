import socket
from ClientSide import ClientSide


class TCP_client():
        def __init__(self, host, port):
            super(TCP_client, self).__init__()
            self.socket = None
            self.HOSTNAME = socket.gethostname()         # current IP
            self.HOST = socket.gethostbyname(self.HOSTNAME)
            self.LISTENING_PORT = 9002    # {port} get from server (should be randomly generated, hardcoded for now)
            self.UDP = 9001               # hardcoded
            self.TCP = (self.HOST, self.LISTENING_PORT)
            self.cs = ClientSide(self.name, self.HOST, self.UDP, self.TCP)

        def run(self):
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
                self.socket.bind((self.HOST, self.LISTENING_PORT))

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
                    conn, address = self.socket.accept()

                    # Prevent timeout from happening
                    self.socket.setblocking(1)

                    print("Connection has been established with IP: " + address[0] + " | Port : " + str(address[1]))

                    # Put file transfer function here.
                    self.sendFile(conn)
                    conn.close()

                except:
                    print("Error accepting connections")


        def sendFile(conn):
            # TODO Change to Json dicts
            fileName = input(str("Please Enter the File Name Of the File you want to trasnfer"))
            file = open(fileName, 'rb')
            fileData = file.read(200)
            conn.send(fileData)
            print("Data Has been transmitted Successfully")


        # ------------------------TCP-------------------------------
        #       PEER COMMUNICATION - Acting Client Side
        # ----------------------------------------------------------
        def sendingClient(self):
            sendingSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sendingHost = input(str("Please enter the host address of the sender"))
            sendingPort = 8081
            s.connect((host, port))
            print("Connected..")

            fileName = input(str("Please enter a filename for the incoming file: "))
            file = open(fileName, 'wb')
            fileData = s.recv(200)
            file.write(fileData)
            file.close()
            print("File has been received successfully")


