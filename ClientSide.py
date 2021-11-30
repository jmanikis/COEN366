from Client import Client
from CDBHelper import CDBHelper
import uuid

#   Provide means for a produce an appropriate dictioinary 
#   for the command request that will be sent to the server

class ClientSide:

    def __init__(self, name, ip, udp, tcp, files=None):
        if files is None:
            files = []
        self.name = name
        self.ip = ip
        self.udp_socket = udp
        self.tcp_socket = tcp
        self.CDBH = CDBHelper()
        self.files = files
        self.SEARCH_FILE_name = None
        # RQ
        self.pending_rq = []
        self.RQ = str(uuid.uuid4())

    # Use: request_dict = cs_obj.REGISTER() to get a dict to send to server.
    def REGISTER(self):
        return self.generate_request(
            "REGISTER",   ip=self.ip, udp_socket=self.udp_socket, tcp_socket=self.tcp_socket)

    # Use: request_dict = cs_obj.DE_REGISTER() to get a dict to send to server.
    def DE_REGISTER(self):
        return self.generate_request("DE-REGISTER")

    # Use: request_dict = cs_obj.PUBLISH(file_list) to get a dict to send to server.
    def PUBLISH(self, files=None):
        if files is None:
            files = self.files
        return self.generate_request("PUBLISH", files=files)

    # Use: request_dict = cs_obj.REMOVE(files_list) to get a dict to send to server.
    def REMOVE(self, files):
        if not type(files) == list:
            files = [files]
        return self.generate_request("REMOVE", files=files)

    # Use: request_dict = cs_obj.RETRIEVE_ALL() to get a dict to send to server.
    def RETRIEVE_ALL(self):
        return self.generate_request("RETRIEVE-ALL")

    # Use: request_dict = cs_obj.SEARCH_FILE(file_name_str) to get a dict to send to server.
    def SEARCH_FILE(self, file_name):
        self.SEARCH_FILE_name = file_name
        return self.generate_request("SEARCH-FILE", file_name=file_name)

    # Use: request_dict = cs_obj.RETRIEVE_INFOT(client_name_str) to get a dict to send to server.
    def RETRIEVE_INFOT(self, client_name):
        return self.generate_request("RETRIEVE-INFOT", client_name=client_name)

    # Use: request_dict = cs_obj.UPDATE_CONTACT() to get a dict to send to server.
    # Note: Can optionally pass params to func for update
    def UPDATE_CONTACT(self, ip=None, udp_socket=None, tcp_socket=None):
        if ip is None:
            ip = self.ip
        else:
            self.ip = ip
        if udp_socket is None:
            udp_socket = self.udp_socket
        else:
            self.udp_socket = udp_socket
        if tcp_socket is None:
            tcp_socket = self.tcp_socket
        else:
            self.tcp_socket = tcp_socket
        return self.generate_request("UPDATE-CONTACT", ip=ip, udp_socket=udp_socket, tcp_socket=tcp_socket)

    # Use: Initiate a download request
    def DOWNLOAD(self, file_name):
        return self.generate_request("DOWNLOAD",  file_name=file_name)
        pass

    # Use: Generate file chunks for the corresponding file 
    def FILE(self, file_name, chunks):
        requests = []
        for chunk in chunks[:-1]:
            chunk_number = chunk[0]
            text = chunk[1]
            request = self.generate_request("FILE", file_name=file_name, chunk_number=chunk_number, text=text)
            requests.append(request)
        last_chunk = chunks[-1][0]
        last_text = chunks[-1][1]
        last_request = self.generate_request(
            "FILE-END", file_name=file_name, chunk_number=last_chunk, text=last_text)
        requests.append(last_request)
        return requests

    #   Return an error if the download was not successful
    def DOWNLOAD_ERROR(self, message):
        return [self.generate_request("DOWNLOAD-ERROR", reason=message)]

    #   Return a client name from a file
    def get_client_from_file_name(self, file_name):
        return self.CDBH.get_client_from_file_name(file_name)

    #   Return a dictionary containing relevant fields to the request
    def generate_request(self, header, **kwargs):
        new_rq = True
        RQ = self.RQ
        print(f"PENDING: {self.pending_rq}")
        existing_request = next((req for req in self.pending_rq if req['header'] == header), None)
        if existing_request is not None:
            RQ = existing_request['RQ']
            new_rq = False
        else:
            self.RQ = str(uuid.uuid4())
        reply = {'header': header, 'RQ': RQ, 'name': self.name}
        reply.update(kwargs)
        if header != "DE-REGISTER" and new_rq:
            self.pending_rq.append(reply)
        return reply

    #   Parse an incoming reply from a client or server 
    #   and return the appropriate header or client 
    #   helper function
    def parse_reply(self, dict_in):
        if dict_in is None:
            return None
        header = dict_in['header']
        self.handle_rq(dict_in)
        try:
            assert type(header) == str
        except Exception as e:
            print(f"Exception in ClientSide.parse_reply: {e}")
            return e
        if "DENIED" in header or "ERROR" in header:
            return f"{header}: {dict_in['reason']}"
        elif header == "REGISTERED":
            return header
        elif header == "PUBLISHED":
            return header
        elif header == "REMOVED":
            return header
        elif header == "RETRIEVE":
            data = dict_in['data']
            self.CDBH.RETRIEVE(data)
            return header
        elif header == "SEARCH-FILE":
            data = dict_in['data']
            self.CDBH.SEARCH_FILE(self.SEARCH_FILE_name, data)
            return header
        elif header == "RETRIEVE-INFOT":
            name = dict_in['name']
            ip = dict_in['ip']
            tcp_socket = dict_in['tcp_socket']
            files = dict_in['files']
            self.CDBH.RETRIEVE_INFOT(name, ip, tcp_socket, files)
            return header
        elif header == "UPDATE-CONFIRMED":
            return header
        elif header == "DOWNLOAD":
            RQ = dict_in['RQ']
            file_name = dict_in['file_name']
            check, reply = self.CDBH.DOWNLOAD(file_name)
            if check:
                return self.FILE(file_name, reply)
            else:
                return self.DOWNLOAD_ERROR(reply)
        elif header == "FILE":
            RQ = dict_in['RQ']
            file_name = dict_in['file_name']
            chunk_number = dict_in['chunk_number']
            text = dict_in['text']
            self.CDBH.FILE(RQ, file_name, chunk_number, text)
        elif header == "FILE-END":
            RQ = dict_in['RQ']
            file_name = dict_in['file_name']
            chunk_number = dict_in['chunk_number']
            text = dict_in['text']
            return self.CDBH.FILE_END(RQ, file_name, chunk_number, text)

    #   Check if the RQ exists in the list of RQ and increment if acknowledged by the server
    def handle_rq(self, dict_in):
        RQ = dict_in['RQ']
        existing_request = next((req for req in self.pending_rq if req['RQ'] == RQ), None)
        print(f"PENDING: {self.pending_rq}")
        if existing_request is not None:
            self.pending_rq.remove(existing_request)
            print(f"PENDING: {self.pending_rq}")
