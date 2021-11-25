from UDP_client import UDP_client
from TCP_client import TCP_client
import socket
import tkinter as tk

class OmegaClient:
    def __init__(self):
        self.HOSTNAME = socket.gethostname()
        self.HOST = socket.gethostbyname(self.HOSTNAME)
        self.UDP_port = 9001
        self.TCP_port = 9091
        self.TCP_client = None
        self.UDP_client = None
        self.server_host = None
        self.server_port = None
        self.name = None
        # GUI
        self.status = "Waiting for initial settings."
        self.window = tk.Tk()
        # Frames
        self.name_frame = tk.Frame(master=self.window)
        self.TCP_frame = tk.Frame(master=self.window)
        self.UDP_frame = tk.Frame(master=self.window)
        self.save_frame = tk.Frame(master=self.window)
        self.ip_frame = tk.Frame(master=self.window)
        # Labels
        self.tk_name = tk.Label(text="Client Name: ", master=self.name_frame)
        self.tk_tcp = tk.Label(text="TCP port: ", master=self.TCP_frame)
        self.tk_udp = tk.Label(text="UDP Port: ", master=self.UDP_frame)
        self.tk_ip = tk.Label(text=f"IP: {self.HOST}", master=self.ip_frame)
        # Text Entries
        self.tk_name_entry = tk.Entry(master=self.name_frame)
        self.tk_TCP_entry = tk.Entry(master=self.TCP_frame)
        self.tk_UDP_entry = tk.Entry(master=self.UDP_frame)
        # Buttons
        self.tk_save_button = tk.Button(text="Save", master=self.save_frame)
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
        # Frames
        self.name_frame.grid(row=0, column=0)
        self.UDP_frame.grid(row=1, column=0)
        self.TCP_frame.grid(row=1, column=1)
        self.ip_frame.grid(row=0, column=1)
        self.save_frame.grid(row=0, column=2)
        self.tk_save_button.bind("<Button-1>", self.save_button)
        self.tk_name.mainloop()

    def save_button(self, event):
        self.name = self.tk_name_entry.get()
        self.tk_name['text'] = f"Client name: {self.name}"
        self.UDP_port = self.tk_UDP_entry.get()
        self.tk_udp['text'] = f"UDP port: {self.UDP_port}"
        self.TCP_port = self.tk_TCP_entry.get()
        self.tk_tcp['text'] = f"TCP port: {self.TCP_port}"

        self.TCP_client = TCP_client(
            self.name, self.UDP_port, self.TCP_port, self.HOST, self.server_host, self.server_port)
        self.UDP_client = UDP_client(
            self.name, self.UDP_port, self.TCP_port, self.HOST, self.server_host, self.server_port)


    def init_UDP(self):
        return UDP_client(self.name, self.UDP_port, self.TCP_port, self.HOST, self.server_host, self.server_port)
        pass

    def init_TCP(self):
        pass
