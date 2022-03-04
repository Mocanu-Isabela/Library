from domain.entities import Client
from validation.validators import RepoError


class ClientsFile(object):
    def __init__(self, file_name):  # file_name='Clients.txt'
        self.file_name = file_name

    def read_from_text_file(self):
        with open(self.file_name, "rt") as file:
            clients=[]
            lines = file.readlines()
            for line in lines:
                if len(line) > 1:
                    line = line[:len(line) - 1].split(';')
                    clients.append(Client(int(line[0]), line[1]))
        file.close()
        return clients

    def append_in_text_file(self, client):
        with open(self.file_name, "at") as file:
            file.write(str(client.get_client_id()) + ";" + client.get_name() + '\n')
        file.close()

    def write_in_text_file(self, clients):
        with open(self.file_name, "wt") as file:
            for client in clients:
                file.write(str(client.get_client_id()) + ";" + client.get_name() + '\n')
        file.close()

    def add(self, client):
        clients = self.read_from_text_file()
        if client in clients:
            raise RepoError("This client already exists!")
        self.append_in_text_file(client)

    def remove(self, client):
        clients = self.read_from_text_file()
        if client not in clients:
            raise RepoError("This client doesn't exist!")
        index = clients.index(client)
        clients.pop(index)
        self.write_in_text_file(clients)

    def update(self, client, new_name):
        clients = self.read_from_text_file()
        if client not in clients:
            raise RepoError("This client doesn't exist!")
        client.set_name(new_name)
        self.write_in_text_file(clients)

    def get_all(self):
        clients = self.read_from_text_file()
        return clients[:]

    def get_client_by_id(self, client_id):
        clients = self.read_from_text_file()
        for current_client in clients:
            if int(current_client.get_client_id())==int(client_id):
                return current_client
        raise RepoError("This client doesn't exist!")

    def get_client_by_partial_id(self, client_id):
        clients = self.read_from_text_file()
        client_by_id_list = []
        for current_client in clients:
            current_client_id = str(current_client.get_client_id())
            client_id = str(client_id)
            if client_id in current_client_id:
                client_by_id_list.append(current_client)
        if len(client_by_id_list) == 0:
            raise RepoError("There is no client with this id!")
        return client_by_id_list

    def get_client_by_partial_name(self, client_name):
        clients = self.read_from_text_file()
        client_by_name_list = []
        for current_client in clients:
            current_client_name = current_client.get_name()
            current_client_name=current_client_name.casefold()
            client_name=client_name.casefold()
            if client_name in current_client_name:
                client_by_name_list.append(current_client)
        if len(client_by_name_list) == 0:
            raise RepoError("There is no client with this name!")
        return client_by_name_list

    def get_client_name_by_id(self, client_id):
        clients = self.read_from_text_file()
        for current_client in clients:
            if int(current_client.get_client_id())==int(client_id):
                name = current_client.get_name()
                return name
        raise RepoError("This client doesn't exist!")
