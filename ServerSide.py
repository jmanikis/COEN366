import traceback

from Client import Client
from DBHelper import DBHelper


class ServerSide:

    # Use instruction:
    # Instantiate this class in server init: server_side_obj = ServerSide()
    # Pass a request_dict to .get_reply() to get a reply_dict: reply_dict = server_side_obj.get_reply(request_dict)
    # Send the reply_dict back to client.

    def __init__(self):
        self.dict_in = None
        self.DBH = DBHelper()
        self.reply = None
        self.pending_rq = []

    def get_reply(self, dict_in):
        self.dict_in = dict_in
        header = self.dict_in['header']
        try:
            assert type(header) == str
            if header == "REGISTER":
                reply = self.REGISTER()
            elif header == "DE-REGISTER":
                self.DE_REGISTER()
                reply = None
            elif header == "PUBLISH":
                reply = self.PUBLISH()
            elif header == "REMOVE":
                reply = self.REMOVE()
            elif header == "RETRIEVE-ALL":
                reply = self.RETRIEVE_ALL()
            elif header == "RETRIEVE-INFOT":
                reply = self.RETRIEVE_INFOT()
            elif header == "SEARCH-FILE":
                reply = self.SEARCH_FILE()
            elif header == "UPDATE-CONTACT":
                reply = self.UPDATE_CONTACT()
            else:
                raise Exception(f"Invalid header: {header}")
            self.reply = reply
            return reply
        except Exception as e:
            print(f"Exception in ServerSide.get_reply: {e}")
            return {"header": "ERROR", "reason": str(e)}

    def REGISTER(self):
        dict_in = self.dict_in
        RQ = None
        try:
            RQ = dict_in['RQ']
            name = dict_in['name']
            ip = dict_in['ip']
            udp = dict_in['udp_socket']
            tcp = dict_in['tcp_socket']
            client = Client(name=name, ip=ip, tcp_socket=tcp, udp_socket=udp, files=None, RQ=RQ)
            check, message = self.DBH.REGISTER(client)
            if check:
                return self.generate_reply("REGISTERED", RQ)
            else:
                return self.generate_reply("REGISTER-DENIED", RQ, reason=message)
        except Exception as e:
            print(f"Exception in ServerSide.REGISTER: {e}")
            return self.generate_reply("REGISTER-DENIED", RQ, reason=str(e))

    def DE_REGISTER(self):
        try:
            dict_in = self.dict_in
            name = dict_in['name']
            check = self.DBH.DE_REGISTER(name)
        except Exception as e:
            print(f"Exception in ServerSide.DE_REGISTER: {e}")
        finally:
            return None

    def PUBLISH(self):
        dict_in = self.dict_in
        RQ = None
        try:
            name = dict_in['name']
            RQ = dict_in['RQ']
            if self.DBH.does_client_exist(dict_in['name']) is None:
                raise Exception("Not registered")
            files = dict_in['files']
            check, message = self.DBH.PUBLISH(name, files)
            if check:
                return self.generate_reply("PUBLISHED", RQ)
            else:
                return self.generate_reply("PUBLISH-DENIED", RQ, reason=message)
        except Exception as e:
            print(f"Exception in ServerSide.PUBLISH: {e}")
            return self.generate_reply("PUBLISH-DENIED", RQ, reason=str(e))

    def REMOVE(self):
        dict_in = self.dict_in
        RQ = None
        try:
            RQ = dict_in['RQ']
            name = dict_in['name']
            if self.DBH.does_client_exist(dict_in['name']) is None:
                raise Exception("Not registered")
            files = dict_in['files']
            check, message = self.DBH.REMOVE(name, files)
            if check:
                return self.generate_reply("REMOVED", RQ)
            else:
                return self.generate_reply("REMOVE-DENIED", RQ, reason=message)
        except Exception as e:
            print(f"Exception in ServerSide.REMOVE: {e}")
            return self.generate_reply("REMOVE-DENIED", RQ, reason=str(e))

    def RETRIEVE_ALL(self):
        dict_in = self.dict_in
        RQ = None
        try:
            RQ = dict_in['RQ']
            if self.DBH.does_client_exist(dict_in['name']) is None:
                raise Exception("Not registered")
            check, response = self.DBH.RETRIEVE_ALL()
            if check:
                return self.generate_reply("RETRIEVE", RQ, data=response)
            else:
                return self.generate_reply("RETRIEVE-ERROR", RQ, reason=response)
        except Exception as e:
            print(f"Exception in ServerSide.RETRIEVE_ALL: {e}")
            return self.generate_reply("RETRIEVE-ERROR", RQ, reason=str(e))

    def SEARCH_FILE(self):
        dict_in = self.dict_in
        RQ = None
        try:
            RQ = dict_in['RQ']
            if self.DBH.does_client_exist(dict_in['name']) is None:
                raise Exception("Not registered")
            file_name = dict_in['file_name']
            check, response = self.DBH.SEARCH_FILE(file_name)
            if check:
                return self.generate_reply("SEARCH-FILE", RQ, data=response)
            else:
                return self.generate_reply("SEARCH-ERROR", RQ, reason=response)
        except Exception as e:
            print(f"Exception in ServerSide.SEARCH_FILE: {e}")
            traceback.print_exc()
            return self.generate_reply("SEARCH-ERROR", RQ, reason=str(e))

    def RETRIEVE_INFOT(self):
        dict_in = self.dict_in
        RQ = None
        try:
            RQ = dict_in['RQ']
            if self.DBH.does_client_exist(dict_in['name']) is None:
                raise Exception("Not registered")
            client_name = dict_in['client_name']
            check, response = self.DBH.RETRIEVE_INFOT(client_name)
            if check:
                ip = response['ip']
                tcp = response['tcp_socket']
                files = response['files']
                return self.generate_reply("RETRIEVE-INFOT", RQ, name=client_name, ip=ip, tcp_socket=tcp, files=files)
            else:
                return self.generate_reply("RETRIEVE-ERROR", RQ, reason=response)
        except Exception as e:
            print(f"Exception in ServerSide.RETRIEVE_INFOT: {e}")
            return self.generate_reply("RETRIEVE-ERROR", RQ, reason=str(e))

    def UPDATE_CONTACT(self):
        dict_in = self.dict_in
        RQ = None
        name = None
        try:
            RQ = dict_in['RQ']
            name = dict_in['name']
            if self.DBH.does_client_exist(dict_in['name']) is None:
                raise Exception("Not registered")
            ip = dict_in['ip']
            udp = dict_in['udp_socket']
            tcp = dict_in['tcp_socket']
            client = Client(name, ip, tcp, udp, None, RQ)
            check, message = self.DBH.UPDATE_CONTACT(client)
            if check:
                return self.generate_reply(
                    "UPDATE-CONFIRMED", RQ, name=name, ip=ip, udp_socket=udp, tcp_socket=tcp)
            else:
                return self.generate_reply("UPDATE-DENIED", RQ, name=name, reason=message)
        except Exception as e:
            print(f"Exception in ServerSide.UPDATE_CONTACT: {e}")
            return self.generate_reply("UPDATE-DENIED", RQ, name=name, reason=str(e))

    def generate_reply(self, header, RQ, **kwargs):
        reply = {'header': header, 'RQ': RQ}
        reply.update(kwargs)
        return reply

    def handle_rq(self, dict_in):
        try:
            RQ = dict_in['RQ']
            name = dict_in['name']

        except Exception as e:
            traceback.print_exc()
            print(e)
