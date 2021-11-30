import ast
import os
import string
import traceback
import random
from pathlib import Path

import TCP_acceptingConnection
import TCP_message_helper
from ClientSide import ClientSide
from UDP_client import UDP_client
from TCP_client import TCP_client
import socket
import tkinter as tk
import UDP_message_helper
import queue
from asyncio import Lock
from server import UDP_server



#        The client GUI used to send commands to 
#        the server.

#           The server button can be used to start a server. 

#        Provides end points for each command specified
#        in the report.
        

class OmegaClient:
    def __init__(self):
        self.HOSTNAME = socket.gethostname()
        self.HOST = socket.gethostbyname(self.HOSTNAME)
        self.UDP_port = None
        self.TCP_port = None
        self.TCP_client = None
        self.UDP_client = None
        self.server_host = None
        self.server_port = None
        self.name = None
        self.client_side = None
        self.server = None
        # Synchronization
        self.cmd_lock = Lock()
        # GUI
        self.status = "Waiting for initial settings."
        self.window = tk.Tk()
        # Frames
        self.name_frame = tk.Frame(master=self.window)
        self.TCP_frame = tk.Frame(master=self.window)
        self.UDP_frame = tk.Frame(master=self.window)
        self.save_frame = tk.Frame(master=self.window)
        self.ip_frame = tk.Frame(master=self.window)
        self.status_frame = tk.Frame(master=self.window)
        self.commands_frame = tk.Frame(master=self.window)
        self.input_frame = tk.Frame(master=self.window)
        self.server_frame = tk.Frame(master=self.window)
        self.info_frame = tk.Frame(master=self.window)
        self.presets_frame = tk.Frame(master=self.window)
        self.files_frame = tk.Frame(master=self.window)
        # Labels
        self.tk_name = tk.Label(text="Client Name: ", master=self.name_frame)
        self.tk_tcp = tk.Label(text="Client TCP port: ", master=self.TCP_frame)
        self.tk_udp = tk.Label(text="Client UDP Port: ", master=self.UDP_frame)
        self.tk_ip = tk.Label(text=f"Client IP: {self.HOST}", master=self.ip_frame)
        self.tk_server_connection = tk.Label(
            text=f"Server connection: {self.server_host}:{self.server_port}", master=self.ip_frame, wraplength=150)
        self.tk_commands = tk.Label(text="Commands List", master=self.commands_frame)
        self.tk_status = tk.Label(text="", master=self.status_frame,
                                  wraplength=300, justify="left")
        self.tk_input = tk.Label(text="Command Input:", master=self.input_frame)
        self.tk_server_settings = tk.Label(text="Server IP:Port", master=self.server_frame)
        self.tk_info = tk.Label(text="", master=self.info_frame, wraplength=300, justify="left")
        self.tk_presets_1 = tk.Label(text="'Start Server' will cause the window to not respond. Closing it will close the server.",
                                     master=self.presets_frame, wraplength=100, justify="left")
        self.tk_presets_2 = tk.Label(text="Client 1-6 will autofill the fields with a sample client. Press save to confirm.",
                                     master=self.presets_frame, wraplength=100, justify="left")
        self.tk_files = tk.Label(text="", master=self.files_frame, wraplength=100, justify="left")
        # Text Entries
        self.tk_name_entry = tk.Entry(master=self.name_frame)
        self.tk_TCP_entry = tk.Entry(master=self.TCP_frame)
        self.tk_UDP_entry = tk.Entry(master=self.UDP_frame)
        self.tk_input_entry = tk.Entry(master=self.input_frame)
        self.tk_server_entry = tk.Entry(master=self.server_frame)
        # Buttons
        self.tk_save_button = tk.Button(text="Save", master=self.save_frame, width=40)
        self.tk_register_button = tk.Button(text="REGISTER", master=self.commands_frame, width=20)
        self.tk_de_register_button = tk.Button(text="DE-REGISTER", master=self.commands_frame, width=20)
        self.tk_publish_button = tk.Button(text="PUBLISH", master=self.commands_frame, width=20)
        self.tk_remove_button = tk.Button(text="REMOVE", master=self.commands_frame, width=20)
        self.tk_retrieve_all_button = tk.Button(text="RETRIEVE ALL", master=self.commands_frame, width=20)
        self.tk_search_file_button = tk.Button(text="SEARCH FILE", master=self.commands_frame, width=20)
        self.tk_retrieve_infot_button = tk.Button(text="RETRIEVE INFO", master=self.commands_frame, width=20)
        self.tk_update_contact_button = tk.Button(text="UPDATE CONTACT", master=self.commands_frame, width=20)
        self.tk_download_button = tk.Button(text="DOWNLOAD", master=self.commands_frame, width=20)
        self.tk_start_server_button = tk.Button(text="Start Server", master=self.presets_frame, width=10)
        self.tk_client1_button = tk.Button(text="Client 1", master=self.presets_frame, width=10)
        self.tk_client2_button = tk.Button(text="Client 2", master=self.presets_frame, width=10)
        self.tk_client3_button = tk.Button(text="Client 3", master=self.presets_frame, width=10)
        self.tk_client4_button = tk.Button(text="Client 4", master=self.presets_frame, width=10)
        self.tk_client5_button = tk.Button(text="Client 5", master=self.presets_frame, width=10)
        self.tk_client6_button = tk.Button(text="Client 6", master=self.presets_frame, width=10)
        self.tk_random_file_button = tk.Button(text="Random File", master=self.files_frame, width=10)
        self.tk_open_folder_button = tk.Button(text="Files Folder", master=self.files_frame, width=10)
        self.init_GUI()

    def init_GUI(self):
        # self.window = tk.Tk()
        # name frame
        self.tk_name.pack()
        self.tk_save_button.pack()
        self.tk_name_entry.pack()
        # TCP frame
        self.tk_tcp.pack()
        self.tk_TCP_entry.pack()
        # UDP frame
        self.tk_udp.pack()
        self.tk_UDP_entry.pack()
        # IP frame
        self.tk_ip.pack()
        self.tk_server_connection.pack()
        # Status frame
        self.tk_status.pack()
        # Commands frame
        self.tk_commands.pack()
        self.tk_register_button.pack()
        self.tk_de_register_button.pack()
        self.tk_publish_button.pack()
        self.tk_remove_button.pack()
        self.tk_retrieve_all_button.pack()
        self.tk_search_file_button.pack()
        self.tk_retrieve_infot_button.pack()
        self.tk_update_contact_button.pack()
        self.tk_download_button.pack()
        # Input frame
        self.tk_input.pack()
        self.tk_input_entry.pack()
        # Server frame
        self.tk_server_settings.pack()
        self.tk_server_entry.pack()
        self.tk_server_entry.insert(0, f":8891")
        # Info frame
        self.tk_info.pack()
        # Preset frame
        self.tk_presets_1.pack()
        self.tk_start_server_button.pack()
        self.tk_presets_2.pack()
        self.tk_client1_button.pack()
        self.tk_client2_button.pack()
        self.tk_client3_button.pack()
        self.tk_client4_button.pack()
        self.tk_client5_button.pack()
        self.tk_client6_button.pack()
        # Files frame
        self.tk_files.pack()
        self.tk_random_file_button.pack()
        self.tk_open_folder_button.pack()
        # Frames
        self.name_frame.grid(row=0, column=0)
        self.UDP_frame.grid(row=1, column=0)
        self.TCP_frame.grid(row=1, column=1)
        self.server_frame.grid(row=0, column=1)
        self.save_frame.grid(row=2, column=0, columnspan=2, sticky=tk.E + tk.W)
        self.ip_frame.grid(row=3, column=1)
        self.commands_frame.grid(row=3, column=0, rowspan=2, sticky=tk.N + tk.S)
        self.input_frame.grid(row=4, column=1)
        self.status_frame.grid(row=5, column=0, columnspan=2, sticky=tk.E + tk.W)
        self.info_frame.grid(row=0, column=3, rowspan=5)
        self.presets_frame.grid(row=0, column=2, rowspan=5, sticky=tk.N + tk.S)
        self.files_frame.grid(row=5, column=2, rowspan=2, sticky=tk.N + tk.S)
        # bind buttons
        self.tk_save_button.bind("<Button-1>", self.save_button)
        self.tk_register_button.bind("<Button-1>", self.register_button)
        self.tk_de_register_button.bind("<Button-1>", self.de_register_button)
        self.tk_publish_button.bind("<Button-1>", self.publish_button)
        self.tk_remove_button.bind("<Button-1>", self.remove_button)
        self.tk_retrieve_all_button.bind("<Button-1>", self.retrieve_all_button)
        self.tk_search_file_button.bind("<Button-1>", self.search_file_button)
        self.tk_retrieve_infot_button.bind("<Button-1>", self.retrieve_infot_button)
        self.tk_update_contact_button.bind("<Button-1>", self.update_contact_button)
        self.tk_download_button.bind("<Button-1>", self.download_button)
        self.tk_start_server_button.bind("<Button-1>", self.start_server_button)
        self.tk_client1_button.bind("<Button-1>", self.client1_button)
        self.tk_client2_button.bind("<Button-1>", self.client2_button)
        self.tk_client3_button.bind("<Button-1>", self.client3_button)
        self.tk_client4_button.bind("<Button-1>", self.client4_button)
        self.tk_client5_button.bind("<Button-1>", self.client5_button)
        self.tk_client6_button.bind("<Button-1>", self.client6_button)
        self.tk_random_file_button.bind("<Button 1>", self.random_file_button)
        self.tk_open_folder_button.bind("<Button 1>", self.open_folder_button)
        # Start GUI
        self.get_files()
        self.set_status("Awaiting user input: Client Name, UDP and TCP ports, server info.")
        self.tk_name.mainloop()

    
    #   Save button allows the client to save the following values:
    #   Client Name
    #   Client UDP port 
    #   Client TCP port 
    #   Server IP 
    #   Server UDP Port
    #   Start TCP accepting thread to listen for download requests
    def save_button(self, event):
        try:
            self.name = self.tk_name_entry.get()                # Save Client name
            self.TCP_port = self.tk_TCP_entry.get()             
            self.UDP_port = self.tk_UDP_entry.get()             
            ip_port = self.tk_server_entry.get().split(':')     
            if len(ip_port) != 2:
                raise Exception("Invalid Server IP:Port")
            self.server_host = ip_port[0]                       # Save Server IP
            self.server_port = int(ip_port[1])                  # Save Server Port
            if self.name == "":
                self.set_status("Name can't be blank.")
            if len(self.UDP_port) > 5 or len(self.TCP_port) > 5:
                self.set_status("Please enter valid port values.")
            elif self.UDP_port == "" or self.TCP_port == "":
                self.set_status("Please enter valid port values.")
            elif self.TCP_port == self.UDP_port:
                raise Exception("Ports cannot be the same.")
            else:
                self.tk_server_connection['text'] = f"Server connection: {self.server_host}:{self.server_port}"
                self.TCP_port = int(self.TCP_port)             # Save Client TCP port
                self.UDP_port = int(self.UDP_port)             # Save Client UDP port
                self.client_side = ClientSide(self.name, self.HOST, self.UDP_port, self.TCP_port)
                self.TCP_client = TCP_client(self.client_side)
                self.UDP_client = UDP_client(self.client_side, self.server_host, self.server_port)
                if self.TCP_client is not None and self.UDP_client is not None:
                    self.set_status("Awaiting command.")
                    self.startTCP_acceptingThread()            # Start TCP accepting thread
            self.tk_name['text'] = f"Client name: {self.name}"
            self.tk_udp['text'] = f"Client UDP port: {self.UDP_port}"
            self.tk_tcp['text'] = f"Client TCP port: {self.TCP_port}"
        except Exception as e:
            traceback.print_exc()
            self.set_status(f"Error: {e}")


    #   Starts a new thread to send "REGISTER" command to the server
    #   Return the reply and set it's status
    def register_button(self, event):
        if self.check_UDP():
            self.set_status("Registering...")
            message = self.UDP_client.message_builder("1")
            reply = self.startThread(message)   
            print("REGISTER_BUTTON " + str(reply))
        else:
            reply = "Name and ports, buddy."
        self.set_status(reply)
        print("register")

    #   Starts a new thread to send "DE-REGISTER" command to the server
    #   Return the reply and set it's status
    def de_register_button(self, event):
        if self.check_UDP():
            self.set_status("De-registering...")
            message = self.UDP_client.message_builder("2")
            reply = self.startThread(message)
        else:
            reply = "Name and ports, buddy."
        self.set_status(reply)
        print("deregister")
        pass

    #   Starts a new thread to send "PUBLISH" command to the server
    #   Return the reply and set it's status
    def publish_button(self, event):
        if self.check_UDP():
            self.set_status("Publishing...")
            user_input = self.tk_input_entry.get()
            if user_input == "" or user_input is None:
                reply = "User input must be name of file(s)."
            else:
                user_input = user_input.split(',')
                user_input = [s.strip() for s in user_input]
                message = self.UDP_client.message_builder("3", user_input)
                reply = self.startThread(message)
        else:
            reply = "Name and ports, buddy."
        self.set_status(reply)
        print("publish")
        pass

    #   Starts a new thread to send "REMOVE" command to the server
    #   Return the reply and set it's status
    def remove_button(self, event):
        if self.check_UDP():
            self.set_status("Removing...")
            user_input = self.tk_input_entry.get()
            if user_input == "" or user_input is None:
                reply = "User input must be name of file(s)."
            else:
                user_input = user_input.split(',')
                user_input = [s.strip() for s in user_input]
                message = self.UDP_client.message_builder("4", user_input)
                reply = self.startThread(message)
        else:
            reply = "Name and ports, buddy."
        self.set_status(reply)
        print("remove")
        pass

    #   Starts a new thread to send "RETRIEVE-ALL" command to the server
    #   Return the reply and set it's status
    def retrieve_all_button(self, event):
        if self.check_UDP():
            self.set_status("Retrieving All...")
            message = self.UDP_client.message_builder("5")
            reply = self.startThread(message)
        else:
            reply = "Name and ports, buddy."
        self.set_status(reply)
        print("retrieve all")
        pass

    #   Starts a new thread to send "SEARCH-FILE" command to the server
    #   Return the reply and set it's status
    def search_file_button(self, event):
        if self.check_UDP():
            self.set_status("Searching File...")
            user_input = self.tk_input_entry.get().strip()
            if user_input == "" or user_input is None:
                reply = "User input must be name of a file."
            else:
                message = self.UDP_client.message_builder("6", user_input)
                reply = self.startThread(message)
        else:
            reply = "Name and ports, buddy."
        self.set_status(reply)
        print("search file")
        pass

    #   Starts a new thread to send "RETRIEVE-INFOT" command to the server
    #   Return the reply and set it's status
    def retrieve_infot_button(self, event):
        if self.check_UDP():
            self.set_status("Retrieving Info...")
            user_input = self.tk_input_entry.get().strip()
            if user_input == "" or user_input is None:
                reply = "User input must be name of a client."
            else:
                message = self.UDP_client.message_builder("7", user_input)
                reply = self.startThread(message)
        else:
            reply = "Name and ports, buddy."
        self.set_status(reply)
        print("retrieve info")
        pass


    #   Starts a new thread to send "UPDATE-CONTACT" command to the server
    #   Return the reply and set it's status
    def update_contact_button(self, event):
        if self.check_UDP():
            self.set_status("Updating Contact...")
            message = self.UDP_client.message_builder("8")
            reply = self.startThread(message)
        else:
            reply = "Name and ports, buddy."
        self.set_status(reply)
        print("update contact")
        pass

    #   Starts a new thread to send "DOWNLOAD" command to another client
    #   Return the reply and set it's status
    def download_button(self, event):
        if self.check_UDP():
            self.set_status("Downloading...")
            user_input = self.tk_input_entry.get()
            if user_input == "" or user_input is None:
                reply = "User input must be name of file."
            reply = self.startTCP_receivingThread(user_input)
        self.set_status(reply)
        print("download")
        pass

    #   Start a server with the UDP port 
    def start_server_button(self, event):
        self.set_status("This widow will be unresponsive while acting as a server. Do not close it.")
        self.server = UDP_server(8891)
        self.server.start()
        self.server.join()

    #   Populate the fields with client preset ports
    def client1_button(self, event):
        self.tk_name_entry.delete(0, tk.END)
        self.tk_name_entry.insert(0, "Sample Client 1")
        self.tk_TCP_entry.delete(0, tk.END)
        self.tk_TCP_entry.insert(0, "9091")
        self.tk_UDP_entry.delete(0, tk.END)
        self.tk_UDP_entry.insert(0, "9092")

    #   Populate the fields with client preset ports
    def client2_button(self, event):
        self.tk_name_entry.delete(0, tk.END)
        self.tk_name_entry.insert(0, "Sample Client 2")
        self.tk_TCP_entry.delete(0, tk.END)
        self.tk_TCP_entry.insert(0, "9093")
        self.tk_UDP_entry.delete(0, tk.END)
        self.tk_UDP_entry.insert(0, "9094")

    #   Populate the fields with client preset ports
    def client3_button(self, event):
        self.tk_name_entry.delete(0, tk.END)
        self.tk_name_entry.insert(0, "Sample Client 3")
        self.tk_TCP_entry.delete(0, tk.END)
        self.tk_TCP_entry.insert(0, "9095")
        self.tk_UDP_entry.delete(0, tk.END)
        self.tk_UDP_entry.insert(0, "9096")

    #   Populate the fields with client preset ports
    def client4_button(self, event):
        self.tk_name_entry.delete(0, tk.END)
        self.tk_name_entry.insert(0, "Sample Client 4")
        self.tk_TCP_entry.delete(0, tk.END)
        self.tk_TCP_entry.insert(0, "9097")
        self.tk_UDP_entry.delete(0, tk.END)
        self.tk_UDP_entry.insert(0, "9098")

    #   Populate the fields with client preset ports
    def client5_button(self, event):
        self.tk_name_entry.delete(0, tk.END)
        self.tk_name_entry.insert(0, "Sample Client 5")
        self.tk_TCP_entry.delete(0, tk.END)
        self.tk_TCP_entry.insert(0, "9099")
        self.tk_UDP_entry.delete(0, tk.END)
        self.tk_UDP_entry.insert(0, "9100")

    #   Populate the fields with client preset ports
    def client6_button(self, event):
        self.tk_name_entry.delete(0, tk.END)
        self.tk_name_entry.insert(0, "Sample Client 6")
        self.tk_TCP_entry.delete(0, tk.END)
        self.tk_TCP_entry.insert(0, "9101")
        self.tk_UDP_entry.delete(0, tk.END)
        self.tk_UDP_entry.insert(0, "9102")

    #   Select a random file from the files folder on the computer
    def random_file_button(self, event):
        file_name = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(3)])
        file_name += ".txt"
        file_path = Path(f"./files/{file_name}")
        lower_bound = random.randint(0, 100)
        upper_bound = random.randint(200, 300)
        if file_path.is_file():
            os.remove(file_path)
        with open(file_path, "a") as file:
            file_contents = ""
            for i in range(lower_bound, upper_bound):
                file_contents += f"{i} "
            file.write(file_contents)
        self.get_files()
        self.set_status(f"Generated file \"{file_name}\" in ./files.\nSelect \"Open Folder\" to view.")

    #   Open the directory where the files are contained
    def open_folder_button(self, event):
        os.startfile("files")

    #   Check for empty UDP field
    def check_UDP(self):
        if self.UDP_client is not None:
            return True
        else:
            return False

    #   Display the result of the request at the bottom of the GUI
    def set_status(self, status):
        self.tk_status['text'] = f"Status: {status}"
        info_str = ""
        if type(status) == dict:
            info_str = self.unpack_dict(status, info_str)
        self.tk_info['text'] = info_str

    #   Initialize a UDP_client object containing saved fields
    def init_UDP(self):
        return UDP_client(self.name, self.UDP_port, self.TCP_port, self.HOST, self.server_host, self.server_port)
        pass

    def init_TCP(self):
        pass

    #   Start a new thread to send request to the server, 
    #   and return the value from the reply
    def startThread(self, message):
        que = queue.Queue()
        client = UDP_message_helper.UDP_message_helper(self.UDP_client, message, que)
        client.start()
        reply = que.get()
        return reply

    #   Start a TCP listening - for download requests
    def startTCP_receivingThread(self, input):
        que = queue.Queue()
        client = TCP_message_helper.TCP_message_helper(self.TCP_client, input, que)
        client.start()
        reply = que.get()
        return reply

    #   Start an accepting thread to initialize the TCP connection
    def startTCP_acceptingThread(self):
        conn = TCP_acceptingConnection.TCP_acceptingConnection(self.TCP_client)
        conn.start()

    #   Format the output of the dictionary from the reply
    def unpack_dict(self, dict_in, in_str, depth=0):
        out_str = in_str
        if type(dict_in) == list:
            if len(dict_in) == 0:
                return out_str
            for item in dict_in:
                out_str = self.unpack_dict(item, out_str, depth+1)
                if "---" not in out_str[-5:]:
                    if ".txt" in out_str[-5:]:
                        out_str += ", "
                    else:
                        out_str += "\n---"
        elif type(dict_in) == dict:
            for item in dict_in.keys():
                indent = ""
                if depth > 0:
                    indent = '  '*(depth-1)+'↳'
                out_str += f"\n{indent}{item}: "
                out_str = self.unpack_dict(dict_in[item], out_str, depth+1)
        else:
            out_str += f"{dict_in}"
        return out_str

    #   Return the files contained in the files directory
    def get_files(self):
        files = os.listdir("./files")
        self.tk_files['text'] = f"Files in ./files: {files}"

