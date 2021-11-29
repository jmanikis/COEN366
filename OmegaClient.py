import ast
import traceback
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
        # Labels
        self.tk_name = tk.Label(text="Client Name: ", master=self.name_frame)
        self.tk_tcp = tk.Label(text="Client TCP port: ", master=self.TCP_frame)
        self.tk_udp = tk.Label(text="Client UDP Port: ", master=self.UDP_frame)
        self.tk_ip = tk.Label(text=f"Client IP: {self.HOST}", master=self.ip_frame)
        self.tk_server_connection = tk.Label(
            text=f"Server connection: {self.server_host}:{self.server_port}", master=self.ip_frame, wraplength=150)
        self.tk_commands = tk.Label(text="Commands List", master=self.commands_frame)
        self.tk_status = tk.Label(text="Awaiting user input: Client Name, UDP and TCP ports, server info.", master=self.status_frame,
                                  wraplength=300, justify="left")
        self.tk_input = tk.Label(text="Command Input:", master=self.input_frame)
        self.tk_server_settings = tk.Label(text="Server IP:Port", master=self.server_frame)
        self.tk_info = tk.Label(text="", master=self.info_frame, wraplength=300, justify="left")
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
        self.init_GUI()

    def init_GUI(self):
        # self.window = tk.Tk()
        # name frame
        self.tk_name.pack()
        self.tk_save_button.pack()
        self.tk_name_entry.pack()
        self.tk_name_entry.insert(0, "Sample Client")
        # TCP frame
        self.tk_tcp.pack()
        self.tk_TCP_entry.pack()
        self.tk_TCP_entry.insert(0, "9001")
        # UDP frame
        self.tk_udp.pack()
        self.tk_UDP_entry.pack()
        self.tk_UDP_entry.insert(0, "9002")
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
        self.info_frame.grid(row=0, column=2, rowspan=5, sticky=tk.N + tk.S)
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
        self.tk_name.mainloop()

    def save_button(self, event):
        try:
            self.name = self.tk_name_entry.get()
            self.TCP_port = self.tk_TCP_entry.get()
            self.UDP_port = self.tk_UDP_entry.get()
            ip_port = self.tk_server_entry.get().split(':')
            if len(ip_port) != 2:
                raise Exception("Invalid Server IP:Port")
            self.server_host = ip_port[0]
            self.server_port = int(ip_port[1])
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
                self.TCP_port = int(self.TCP_port)
                self.UDP_port = int(self.UDP_port)
                self.client_side = ClientSide(self.name, self.HOST, self.UDP_port, self.TCP_port)
                self.TCP_client = TCP_client(self.client_side)
                self.UDP_client = UDP_client(self.client_side, self.server_host, self.server_port)
                if self.TCP_client is not None and self.UDP_client is not None:
                    self.set_status("Awaiting command.")
                    self.startTCP_acceptingThread()
            self.tk_name['text'] = f"Client name: {self.name}"
            self.tk_udp['text'] = f"Client UDP port: {self.UDP_port}"
            self.tk_tcp['text'] = f"Client TCP port: {self.TCP_port}"
        except Exception as e:
            traceback.print_exc()
            self.set_status(f"Error: {e}")

    def register_button(self, event):
        if self.check_UDP():
            message = self.UDP_client.message_builder("1")
            # reply = self.UDP_client.send_message(message)
            reply = self.startThread(message)
            print("REGISTER_BUTTON " + str(reply))
        else:
            reply = "Name and ports, buddy."
        self.set_status(reply)
        print("register")

    def de_register_button(self, event):
        if self.check_UDP():
            message = self.UDP_client.message_builder("2")
            # reply = self.UDP_client.send_message(message)
            reply = self.startThread(message)
        else:
            reply = "Name and ports, buddy."
        self.set_status(reply)
        print("deregister")
        pass

    def publish_button(self, event):
        if self.check_UDP():
            user_input = self.tk_input_entry.get()
            if user_input == "" or user_input is None:
                reply = "User input must be name of file(s)."
            else:
                user_input = user_input.split(',')
                user_input = [s.strip() for s in user_input]
                message = self.UDP_client.message_builder("3", user_input)
                # reply = self.UDP_client.send_message(message)
                reply = self.startThread(message)
        else:
            reply = "Name and ports, buddy."
        self.set_status(reply)
        print("publish")
        pass

    def remove_button(self, event):
        if self.check_UDP():
            user_input = self.tk_input_entry.get()
            if user_input == "" or user_input is None:
                reply = "User input must be name of file(s)."
            else:
                user_input = user_input.split(',')
                user_input = [s.strip() for s in user_input]
                message = self.UDP_client.message_builder("4", user_input)
                # reply = self.UDP_client.send_message(message)
                reply = self.startThread(message)
        else:
            reply = "Name and ports, buddy."
        self.set_status(reply)
        print("remove")
        pass

    def retrieve_all_button(self, event):
        if self.check_UDP():
            message = self.UDP_client.message_builder("5")
            # reply = self.UDP_client.send_message(message)
            reply = self.startThread(message)
        else:
            reply = "Name and ports, buddy."
        self.set_status(reply)
        print("retrieve all")
        pass

    def search_file_button(self, event):
        if self.check_UDP():
            user_input = self.tk_input_entry.get().strip()
            if user_input == "" or user_input is None:
                reply = "User input must be name of a file."
            else:
                message = self.UDP_client.message_builder("6", user_input)
                # reply = self.UDP_client.send_message(message)
                reply = self.startThread(message)
        else:
            reply = "Name and ports, buddy."
        self.set_status(reply)
        print("search file")
        pass

    def retrieve_infot_button(self, event):
        if self.check_UDP():
            user_input = self.tk_input_entry.get().strip()
            if user_input == "" or user_input is None:
                reply = "User input must be name of a client."
            else:
                message = self.UDP_client.message_builder("7", user_input)
                # reply = self.UDP_client.send_message(message)
                reply = self.startThread(message)
        else:
            reply = "Name and ports, buddy."
        self.set_status(reply)
        print("retrieve info")
        pass

    def update_contact_button(self, event):
        if self.check_UDP():
            message = self.UDP_client.message_builder("8")
            # reply = self.UDP_client.send_message(message)
            reply = self.startThread(message)
        else:
            reply = "Name and ports, buddy."
        self.set_status(reply)
        print("update contact")
        pass

    def download_button(self, event):
        if self.check_UDP():
            user_input = self.tk_input_entry.get()
            if user_input == "" or user_input is None:
                reply = "User input must be name of file."
            reply = self.startTCP_receivingThread(user_input)
        self.set_status(reply)
        print("download")
        pass

    def check_UDP(self):
        if self.UDP_client is not None:
            return True
        else:
            return False

    def set_status(self, status):
        self.tk_status['text'] = status
        info_str = ""
        if type(status) == dict:
            info_str = self.unpack_dict(status, info_str)
        self.tk_info['text'] = info_str

    def init_UDP(self):
        return UDP_client(self.name, self.UDP_port, self.TCP_port, self.HOST, self.server_host, self.server_port)
        pass

    def init_TCP(self):
        pass

    def startThread(self, message):
        que = queue.Queue()
        client = UDP_message_helper.UDP_message_helper(self.UDP_client, message, que)
        client.start()
        reply = que.get()
        return reply

    def startTCP_receivingThread(self, input):
        que = queue.Queue()
        client = TCP_message_helper.TCP_message_helper(self.TCP_client, input, que)
        client.start()
        reply = que.get()
        return reply

    def startTCP_acceptingThread(self):
        conn = TCP_acceptingConnection.TCP_acceptingConnection(self.TCP_client)
        conn.start()

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

