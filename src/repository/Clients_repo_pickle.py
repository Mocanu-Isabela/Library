from domain.entities import Client
from validation.validators import RepoError
import pickle
import os


class ClientsBinary(object):
    def __init__(self, file_name):  # file_name='Clients.pickle'
        self.file_name = file_name
        self.clients = []
        self.read_from_binary_file()

    def read_from_binary_file(self):
        if os.path.getsize(self.file_name) > 0:
            with open(self.file_name, "rb") as file:
                try:
                    while 1:
                        repo = pickle.load(file)
                        self.clients.append(repo)
                except EOFError:
                    return []
                except IOError as ioe:
                    raise IOError(ioe)
            return repo

    def write_in_binary_file(self, clients):
        # ["id", "name"]
        with open(self.file_name, "wb") as file:
            for client in clients:
                pickle.dump(client, file)
        file.close()

    def add(self, client):
        clients = self.clients
        if client in self.clients:
            raise RepoError("This client already exists!")
        client_id = client.get_client_id()
        name = client.get_name()
        clients.append(Client(int(client_id), name))
        self.write_in_binary_file(clients)

    def remove(self, client):
        if client not in self.clients:
            raise RepoError("This client doesn't exist!")
        index = self.clients.index(client)
        self.clients.pop(index)
        self.write_in_binary_file(self.clients)

    def update(self, client, new_name):
        if client not in self.clients:
            raise RepoError("This client doesn't exist!")
        client.set_name(new_name)
        self.write_in_binary_file(self.clients)

    def get_all(self):
        return self.clients[:]

    def get_client_by_id(self, client_id):
        for current_client in self.clients:
            if int(current_client.get_client_id())==int(client_id):
                return current_client
        raise RepoError("This client doesn't exist!")

    def get_client_by_partial_id(self, client_id):
        client_by_id_list = []
        for current_client in self.clients:
            current_client_id = str(current_client.get_client_id())
            client_id = str(client_id)
            if client_id in current_client_id:
                client_by_id_list.append(current_client)
        if len(client_by_id_list) == 0:
            raise RepoError("There is no client with this id!")
        return client_by_id_list

    def get_client_by_partial_name(self, client_name):
        client_by_name_list = []
        for current_client in self.clients:
            current_client_name = current_client.get_name()
            current_client_name=current_client_name.casefold()
            client_name=client_name.casefold()
            if client_name in current_client_name:
                client_by_name_list.append(current_client)
        if len(client_by_name_list) == 0:
            raise RepoError("There is no client with this name!")
        return client_by_name_list

    def get_client_name_by_id(self, client_id):
        for current_client in self.clients:
            if int(current_client.get_client_id())==int(client_id):
                name = current_client.get_name()
                return name
        raise RepoError("This client doesn't exist!")
