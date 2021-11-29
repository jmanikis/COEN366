import traceback

from tinydb import TinyDB
from tinydb import Query
from Client import Client
from File import File


class DBHelper:
    def __init__(self):
        self.query = Query()
        self.db = TinyDB("server.json")
        self.clients_table = self.db.table("clients")
        self.rq_table = self.db.table("rq")

    # Registration
    def REGISTER(self, client):
        try:
            if self.does_client_exist(client) is None:
                self.clients_table.insert(client)
                return True, None
            else:
                return False, "Already registered."
        except Exception as e:
            traceback.print_exc()
            print(e)
            return False, "Database error."

    def DE_REGISTER(self, client):
        try:
            if self.does_client_exist(client) is None:
                return True
            else:
                if type(client) == str:
                    self.clients_table.remove(self.query.name == client)
                    return True
                elif type(client) == Client or type(client) == dict:
                    self.clients_table.remove(self.query.name == client['name]'])
                    return True
                else:
                    return False
        except Exception as e:
            print(e)
            return False

    # File Related
    def PUBLISH(self, client_name, files):
        try:
            existing_client = self.does_client_exist(client_name)
            if existing_client is None:
                return False, "Client not registered."
            else:
                existing_files = existing_client['files']
            for file in files:
                if file in existing_files:
                    continue
                else:
                    existing_files.append(file)
            self.clients_table.update({'files': existing_files}, self.query.name == client_name)
            return True, None
        except Exception as e:
            print(e)
            traceback.print_exc()
            return False, "Database Error"
        pass

    def REMOVE(self, client, files):
        try:
            existing_client = self.does_client_exist(client)
            if existing_client is not None:
                client_files = existing_client['files']
                try:
                    assert type(files) == list
                except:
                    files = [files]
                for file in files:
                    if file in client_files:
                        client_files.remove(file)
                existing_client['files'] = client_files
                self.UPDATE_CONTACT(existing_client, replace_files=True)
                return True, None
            else:
                return False, "Client not registered."
        except Exception as e:
            print(e)
            traceback.print_exc()
            return False, "Database error."

    # Retrieving Information

    def RETRIEVE_ALL(self):
        list_of_everything = {}
        try:
            all_clients = self.clients_table.all()
            all_clients_stripped = []
            for client in all_clients:
                client = Client.from_dict(client)
                all_clients_stripped.append(client.get_client_data())
            list_of_everything['clients'] = all_clients_stripped
            files_dict = self.get_file_dict()
            list_of_everything['files'] = files_dict
            return True, list_of_everything
        except Exception as e:
            print(e)
            traceback.print_exc()
            return False, "Database error."

    def SEARCH_FILE(self, name):
        client_list = []
        try:
            clients = self.clients_table.search(self.query.files.any([name]))
            for client in clients:
                client = Client.from_dict(client)
                client_list.append(client.get_client_connection())
            return True, client_list
        except Exception as e:
            print(e)
            traceback.print_exc()
            return False, "Database error."

    def RETRIEVE_INFOT(self, name):
        try:
            existing_client = self.does_client_exist(name)
            if existing_client is not None:
                existing_client = existing_client.get_client_data()
                return True, existing_client
            else:
                return False, "Client not registered."
        except Exception as e:
            print(e)
            traceback.print_exc()
            return False, "Database error."

    def UPDATE_CONTACT(self, client, replace_files=False):
        existing_client = self.does_client_exist(client)
        try:
            if existing_client is not None:
                if not replace_files:
                    files = existing_client['files']
                    client['files'] = files
                self.clients_table.remove(self.query.name == client['name'])
                self.clients_table.insert(client)
                print(client)
                return True, None
            else:
                return False, "Client not found."
        except Exception as e:
            print(e)
            traceback.print_exc()
            return False, "Database error."

    # Helper Functions
    def does_client_exist(self, client):
        if type(client) != str:
            client = client['name']
        elif type(client) == str:
            pass
        else:
            print(f"does_client_exist expecting Client or String, received {type(client)}")
            return None
        found_client = self.clients_table.search(self.query.name == client)
        print(found_client)
        if len(found_client) == 1:
            found_client = found_client[0]
            found_client = Client.from_dict(found_client)
            return found_client
        else:
            return None

    def get_file_dict(self):
        files_list = []
        files_dict = {}
        try:
            clients = self.clients_table.all()  # Get full list of all clients and their files
            for client in clients:
                client = Client.from_dict(client)
                files = client['files']   # Get a list of all files from that client
                for file_name in files:
                    if file_name in files_dict:  # If the file has been added to the list already
                        clients_with_file = files_dict[file_name]  # Get the list of clients associated with the file
                        clients_with_file.append(client.get_client_connection())  # Append the new client to the list
                        files_dict[file_name] = clients_with_file  # Reassign the list of clients
                    else:
                        files_dict[file_name] = [client.get_client_connection()]  # put the first client in a list
            for file in files_dict:
                new_file = File(file, files_dict[file])
                files_list.append(new_file)
        except Exception as e:
            print(e)
            traceback.print_exc()
        finally:
            return files_list

    def save_rq(self, dict_in):
        try:
            print(f"SAVE_RQ_1: {self.rq_table.all()}")
            RQ = dict_in['RQ']
            name = dict_in['name']
            existing_client = self.rq_table.search(self.query.name == name)
            if len(existing_client) == 1:
                existing_client = existing_client[0]
                rqs = existing_client['rqs']
                for item in rqs:
                    if RQ in item:
                        if item[RQ]:
                            return True
                        else:
                            return False
                rqs.append({RQ: False})
                self.rq_table.update({'rqs': rqs}, self.query.name == name)
            elif len(existing_client) == 0:
                self.rq_table.insert({'name': name, 'rqs': [{RQ: False}]})
            else:
                pass
            print(f"SAVE_RQ_2: {self.rq_table.all()}")
        except Exception as e:
            traceback.print_exc()
            print(e)

    def set_rq(self, dict_in):
        try:
            print(f"SET_RQ_1: {self.rq_table.all()}")
            RQ = dict_in['RQ']
            name = dict_in['name']
            existing_client = self.rq_table.search(self.query.name == name)
            if len(existing_client) == 1:
                existing_client = existing_client[0]
                rqs = existing_client['rqs']
                to_update = None
                for item in reversed(rqs):
                    if RQ in item:
                        to_update = item
                        break
                if to_update is not None:
                    print(f"to_update: {to_update}")
                    rqs.remove(to_update)
                    rqs.append({RQ: True})
                    self.rq_table.update({'rqs': rqs}, self.query.name == name)
                else:
                    raise Exception("Somehow completed a RQ without it being in this list?")
            else:
                raise Exception("Somehow processed a request from a non-registered user?")
            print(f"SET_RQ_2: {self.rq_table.all()}")
        except Exception as e:
            traceback.print_exc()
            print(e)

