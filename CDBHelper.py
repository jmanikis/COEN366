from tinydb import TinyDB
from tinydb import Query
from Client import Client
from pathlib import Path
import os


class CDBHelper:

    def __init__(self):
        self.query = Query()
        self.db = TinyDB("db.json")
        self.clients_table = self.db.table("clients")
        self.files_table = self.db.table("files")
        self.download_table = self.db.table("downloads")
        self.path = Path("./files")

    def RETRIEVE(self, data):
        try:
            self.clients_table.truncate()
            self.files_table.truncate()
            clients = data['clients']
            files = data['files']
            for client in clients:
                self.clients_table.insert(client)
            for file in files:
                self.files_table.insert(file)
        except Exception as e:
            print(e)

    def SEARCH_FILE(self, file_name, data):
        try:
            assert type(data) == list
            self.files_table.upsert({'clients': data}, self.query.name == file_name)
        except Exception as e:
            print(e)

    def RETRIEVE_INFOT(self, name, ip, tcp_socket, files):
        try:
            existing_client = self.does_client_exist(name)
            if existing_client is not None:
                self.clients_table.remove(self.query.name == name)
            client = Client(name, ip, tcp_socket, files=files)
            self.clients_table.insert(client)
        except Exception as e:
            print(e)

    def DOWNLOAD(self, file_name):
        try:
            if not self.path.is_dir():
                os.mkdir(self.path)
            file_path = Path(os.path.join(self.path, f"/{file_name}"))
            iterator = 1
            chunks = []
            with open(file_path) as file:
                while True:
                    chunk = file.read(200)
                    if not chunk:
                        break
                    chunks.append((iterator, chunk))
                    iterator += 1
            return True, chunks
        except Exception as e:
            print(e)
            return False, "Download error."

    def FILE(self, RQ, file_name, chunk_number, text):
        chunk = {"RQ": RQ, "file_name": file_name, "chunk_number": chunk_number, "text": text}
        self.download_table.insert(chunk)

    def FILE_END(self, RQ, file_name, chunk_number, text):
        try:
            last_chunk = {"RQ": RQ, "file_name": file_name, "chunk_number": chunk_number, "text": text}
            file_key = {"RQ": RQ, "file_name": file_name}
            chunks = self.download_table.search(self.query.fragment(file_key))
            chunks.append(last_chunk)

            chunk_list = []
            for chunk in chunks:
                chunk_list.append((chunk['chunk_number'], chunk['text']))
            chunk_list.sort(key=lambda x: x[0])

            file_path = Path(os.path.join(self.path, f"/{file_name}"))
            if file_path.is_file():
                os.remove(file_path)

            with(file_path, "a") as file:
                for chunk in chunk_list:
                    file.write(chunk[1])

            self.download_table.remove(self.query.fragment(file_key))
        except Exception as e:
            print(e)

    def get_client_from_file_name(self, file_name):
        file = self.files_table.search(self.query.name == file_name)
        if len(file) == 0:
            return None
        else:
            clients = file[0]['clients']
            if len(clients) == 0:
                return None
            else:
                return clients[0]

    def does_client_exist(self, client):
        if type(client) != str:
            client = client['name']
        elif type(client) == str:
            pass
        else:
            print(f"does_client_exist expecting Client or String, received {type(client)}")
            return None
        found_client = self.clients_table.search(self.query.name == client)
        if len(found_client) == 1:
            return found_client[0]
        else:
            return None
