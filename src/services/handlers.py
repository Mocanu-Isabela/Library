import configparser

type = 0

config = configparser.ConfigParser()
config.read("setting.properties")

variable = config["Default"]

filetype = variable["repository"]

file_for_books = variable["books"]
file_for_books = file_for_books.replace("\"", "")

file_for_clients = variable["clients"]
file_for_clients = file_for_clients.replace("\"", "")

file_for_rentals = variable["rentals"]
file_for_rentals = file_for_rentals.replace("\"", "")

def get_type():
    return filetype

def get_file_for_books():
    print(file_for_books)
    return file_for_books

def get_file_for_clients():
    return file_for_clients

def get_file_for_rentals():
    return file_for_rentals