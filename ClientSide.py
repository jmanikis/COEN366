from Client import Client
from CDBHelper import CDBHelper
import random


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
        self.RQ = None
        self.SEARCH_FILE_name = None

    def REGISTER(self):
        return self.generate_request(
            "REGISTER", self.RQ, name=self.name, ip=self.ip, udp_socket=self.udp_socket, tcp_socket=self.tcp_socket)

    def DE_REGISTER(self):
        return self.generate_request("DE-REGISTER", self.RQ, name=self.name)

    def PUBLISH(self, files=None):
        if files is None:
            files = self.files
        return self.generate_request("PUBLISH", self.RQ, files=files)

    def REMOVE(self, files):
        if not type(files) == list:
            files = [files]
        return self.generate_request("REMOVE", self.RQ, files=files)

    def RETRIEVE_ALL(self):
        return self.generate_request("RETRIEVE-ALL", self.RQ)

    def SEARCH_FILE(self, file_name):
        self.SEARCH_FILE_name = file_name
        return self.generate_request("SEARCH_FILE", self.RQ, file_name=file_name)

    def RETRIEVE_INFOT(self, name):
        return self.generate_request("RETRIEVE_INFOT", self.RQ, name=name)

    def UPDATE_CONTACT(self):
        return self.generate_request(
            "UPDATE-CONTACT",
            self.RQ,
            name=self.name,
            ip=self.ip,
            udp_socket=self.udp_socket,
            tcp_socket=self.tcp_socket)

    def DOWNLOAD(self, file_name):
        return self.generate_request("DOWNLOAD", self.RQ, file_name=file_name)
        pass

    def FILE(self, RQ, file_name, chunks):
        requests = []
        for chunk in chunks[:-1]:
            chunk_number = chunk[0]
            text = chunk[1]
            request = self.generate_request("FILE", RQ, file_name=file_name, chunk_number=chunk_number, text=text)
            requests.append(request)
        last_chunk = chunks[-1][0]
        last_text = chunks[-1][1]
        last_request = self.generate_request(
            "FILE-END", RQ, file_name=file_name, chunk_number=last_chunk, text=last_text)
        requests.append(last_request)
        return requests

    def DOWNLOAD_ERROR(self, RQ, message):
        return self.generate_request("DOWNLOAD-ERROR", RQ, reason=message)

    def generate_request(self, header, RQ, **kwargs):
        reply = {'header': header, 'RQ': RQ}
        reply.update(kwargs)
        return reply

    def parse_reply(self, dict_in):
        header = dict_in['header']
        try:
            assert type(header) == str
        except Exception as e:
            print(f"Exception in ClientSide.parse_reply: {e}")
            return
        if "DENIED" in header or "ERROR" in header:
            pass
        elif header == "REGISTERED":
            pass
        elif header == "PUBLISHED":
            pass
        elif header == "REMOVED":
            pass
        elif header == "RETRIEVE":
            data = dict_in['data']
            self.CDBH.RETRIEVE(data)
        elif header == "SEARCH-FILE":
            data = dict_in['data']
            self.CDBH.SEARCH_FILE(self.SEARCH_FILE_name, data)
        elif header == "RETRIEVE-INFOT":
            name = dict_in['name']
            ip = dict_in['ip']
            tcp_socket = dict_in['tcp_socket']
            files = dict_in['files']
            self.CDBH.RETRIEVE_INFOT(name, ip, tcp_socket, files)
        elif header == "UPDATE-CONFIRMED":
            pass
        elif header == "DOWNLOAD":
            RQ = dict_in['RQ']
            file_name = dict_in['file_name']
            check, reply = self.CDBH.DOWNLOAD(file_name)
            if check:
                return self.FILE(RQ, file_name, reply)
            else:
                return self.DOWNLOAD_ERROR(RQ, reply)
            pass
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
            self.CDBH.FILE_END(RQ, file_name, chunk_number, text)
        else:
            pass
