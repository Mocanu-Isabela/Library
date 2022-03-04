"""
4. Library
Write an application for a book library. The application will store:

Book: book_id, title, author
Client: client_id, name
Rental: rental_id, book_id, client_id, rented_date, returned_date
Create an application to:

1.Manage clients and books. The user can add, remove, update, and list both clients and books.
2.Rent or return a book. A client can rent an available book. A client can return a rented book at any time. Only available books can be rented.
3.Search for clients or books using any one of their fields (e.g. books can be searched for using id, title or author). The search must work using case-insensitive, partial string matching, and must return all matching items.
4.Create statistics:
    Most rented books. This will provide the list of books, sorted in descending order of the number of times they were rented.
    Most active clients. This will provide the list of clients, sorted in descending order of the number of book rental days they have (e.g. having 2 rented books for 3 days each counts as 2 x 3 = 6 days).
    Most rented author. This provides the list of books authored, sorted in descending order of the number of rentals their books have.
5.Unlimited undo/redo functionality. Each step will undo/redo the previous operation performed by the user. Undo/redo operations must cascade and have a memory-efficient implementation (no superfluous list copying).
"""
from testss.test import Tests
from testss.tests_a10module import IterableDataStructureTests, GnomeSortAndFilterTests
from validation.validators import ValidatorBook, ValidatorClient, ValidatorRental, ValidError, RepoError, ServError
from repository.repos import RepoBook, RepoClient, RepoRental
from services.service import ServiceBook, ServiceClient, ServiceRental
from services.handlers import get_type, get_file_for_books, get_file_for_clients, get_file_for_rentals
from repository.Books_repo_file import BooksFile
from repository.Clients_repo_file import ClientsFile
from repository.Rentals_repo_file import RentalsFile
from repository.Books_repo_pickle import BooksBinary
from repository.Clients_repo_pickle import ClientsBinary
from repository.Rentals_repo_pickle import RentalsBinary

import random
import sys


class MenuColors:
    BLACK = '\33[30m'
    RED = '\33[31m'
    LEMON = '\33[32m'
    YELLOW = '\33[33m'
    BLUE = '\33[34m'
    VIOLET = '\33[35m'
    TURQUOISE = '\33[36m'
    GREY = '\33[37m'
    LIGHTBLUE = '\033[38;5;116m'
    END = '\033[0m'


class UI:
    def __init__(self, servBook, servClient, servRental):
        self.__servBook = servBook
        self.__servClient = servClient
        self.__servRental = servRental

    def print_main_menu(self):
        menu_string = '\n' + MenuColors.LIGHTBLUE + 'Menu:\n' + MenuColors.END
        menu_string += '\t' + MenuColors.RED + 'add client id name' + MenuColors.END + ' - Add a new client with the given name.\n'
        menu_string += '\t' + MenuColors.RED + 'remove client id' + MenuColors.END + ' - Remove the client with the given id.\n'
        menu_string += '\t' + MenuColors.RED + 'update client id new_name' + MenuColors.END + ' - Update a client`s name with the given new name.\n'
        menu_string += '\t' + MenuColors.RED + 'list clients' + MenuColors.END + ' - List all clients.\n'
        menu_string += '\t' + MenuColors.VIOLET + 'add book' + MenuColors.END + ' - Add a new book.\n'
        menu_string += '\t' + MenuColors.VIOLET + 'remove book id' + MenuColors.END + ' - Remove the book with the given id.\n'
        menu_string += '\t' + MenuColors.VIOLET + 'update book' + MenuColors.END + ' - Update a book`s title and author.\n'
        menu_string += '\t' + MenuColors.VIOLET + 'list books' + MenuColors.END + ' - List all books.\n'
        menu_string += '\t' + MenuColors.TURQUOISE + 'rent rental_id rent_date book_id client_id' + MenuColors.END + ' - The client that has that client_id rents a book with the given book_id, the dates should be in the form dd.mm.yyyy.\n'
        menu_string += '\t' + MenuColors.TURQUOISE + 'return rental_id return_date book_id client_id' + MenuColors.END + ' - The client that has that client_id returns a book with the given book_id, the dates should be in the form dd.mm.yyyy.\n'
        menu_string += '\t' + MenuColors.TURQUOISE + 'list rentals' + MenuColors.END + ' - List all rentals.\n'
        menu_string += '\t' + MenuColors.YELLOW + 'search book by id' + MenuColors.END + ' - Search for a book by entering a part of its id.\n'
        menu_string += '\t' + MenuColors.YELLOW + 'search book by title' + MenuColors.END + ' - Search for a book by entering a part of its title.\n'
        menu_string += '\t' + MenuColors.YELLOW + 'search book by author' + MenuColors.END + ' - Search for a book by entering a part of its author.\n'
        menu_string += '\t' + MenuColors.YELLOW + 'search client by id' + MenuColors.END + ' - Search for a client by entering a part of its id.\n'
        menu_string += '\t' + MenuColors.YELLOW + 'search client by name' + MenuColors.END + ' - Search for a client by entering a part of its name.\n'
        menu_string += '\t' + MenuColors.BLUE + 'most rented books' + MenuColors.END + ' - Print most rented books.\n'
        menu_string += '\t' + MenuColors.BLUE + 'most rented authors' + MenuColors.END + ' - Print most rented authors.\n'
        menu_string += '\t' + MenuColors.BLUE + 'most active clients' + MenuColors.END + ' - Print most active clients.\n'
        menu_string += '\t' + MenuColors.GREY + 'undo' + MenuColors.END + ' - Undo the last operation that modified program data. This step can be repeated\n'
        menu_string += '\t' + MenuColors.GREY + 'redo' + MenuColors.END + ' - Redo the last operation that was undone. This step can be repeated\n'
        menu_string += '\t 0 - Exit\n'
        print(menu_string)

    def start(self):
        input_type = get_type()
        if input_type == "inmemory":
            self.generate_book_list()
            self.generate_client_list()
        elif input_type == "textfile":
            pass
        elif input_type == "binaryfile":
            pass
        else:
            sys.exit("Something is wrong with the files.")
        undo_list = []
        redo_list = []
        times_undo = 0
        times_redo = 0

        stop = False
        while not stop:
            self.print_main_menu()
            ui_command = input("Please enter a command: ")
            c = ui_command.split()

            if len(c) == 0:
                print("Invalid command!")
            elif c[0] == '0' and len(c) == 1:
                print("Have a nice day! :)")
                stop = True
            elif len(c) < 2 and c[0] != 'undo' and c[0] != 'redo':
                print("Invalid command!")
            elif c[0] == 'add' and c[1] == 'client' and len(c) >= 4:
                try:
                    client_id = int(c[2])
                    client_name = c[3:]
                    name = ""
                    for i in client_name:
                        name += str(i)
                        name += ' '
                    self.__servClient.add_client(client_id, name)
                    yes_or_no = "no"
                    param_2 = ["-", "-", "-"]
                    function_and_param = ["remove client", [client_id, name], yes_or_no, param_2]
                    undo_list.append(function_and_param)
                    times_undo = times_undo + 1
                    redo_list.clear()
                    times_redo = 0
                except ValueError:
                    print("The id has to be an integer")
                except ValidError as ve:
                    print(ve)
                except RepoError as re:
                    print(re)
            elif c[0] == 'remove' and c[1] == 'client' and len(c) == 3:
                type_book_or_client = "client"
                client_id = int(c[2])
                try:
                    name = self.__servClient.get_client_full_name_by_id(client_id)
                    param = self.__servRental.check_rentals_after_book_or_client_removes(type_book_or_client, client_id)
                    self.__servClient.remove_client(client_id)
                    yes_or_no = param[0]
                    rental_id = param[1]
                    rent_date = param[2]
                    book_id = param[3]
                    if yes_or_no == "yes":
                        param_2 = [rental_id, rent_date, book_id]
                    else:
                        param_2 = ["-", "-", "-"]
                    function_and_param = ["add client", [client_id, name], yes_or_no, param_2]
                    undo_list.append(function_and_param)
                    times_undo = times_undo + 1
                    redo_list.clear()
                    times_redo = 0
                except ValueError:
                    print("The id has to be an integer")
                except ValidError as ve:
                    print(ve)
                except RepoError as re:
                    print(re)
            elif c[0] == 'update' and c[1] == 'client' and len(c) >= 4:
                try:
                    client_id = int(c[2])
                    old_name = self.__servClient.get_client_full_name_by_id(client_id)
                    name = c[3:]
                    new_name = ""
                    for i in name:
                        new_name += str(i)
                        new_name += ' '
                    self.__servClient.update_client(client_id, new_name)
                    function_and_param = ["update client", [client_id, old_name, new_name]]
                    undo_list.append(function_and_param)
                    times_undo = times_undo + 1
                    redo_list.clear()
                    times_redo = 0
                except ValueError:
                    print("The id has to be an integer")
                except ValidError as ve:
                    print(ve)
                except RepoError as re:
                    print(re)
            elif c[0] == 'list' and c[1] == 'clients' and len(c) == 2:
                clients_list = self.__servClient.get_all_clients()
                if len(clients_list) == 0:
                    print("There is no client!")
                else:
                    for i in clients_list:
                        print(str(i))
            elif c[0] == 'add' and c[1] == 'book' and len(c) == 2:
                try:
                    book_id = int(input("Please enter an id: "))
                    title = str(input("Please enter a book title: "))
                    author = str(input("Please enter the book's author: "))
                    self.__servBook.add_book(book_id, title, author)
                    yes_or_no = "no"
                    param_2 = ["-", "-", "-"]
                    function_and_param = ["remove book", [book_id, title, author], yes_or_no, param_2]
                    undo_list.append(function_and_param)
                    times_undo = times_undo + 1
                    redo_list.clear()
                    times_redo = 0
                except ValueError:
                    print("The id has to be an integer")
                except ValidError as ve:
                    print(ve)
                except RepoError as re:
                    print(re)
            elif c[0] == 'remove' and c[1] == 'book' and len(c) == 3:
                type_book_or_client = "book"
                book_id = int(c[2])
                try:
                    title = self.__servBook.get_book_full_title_by_id(book_id)
                    author = self.__servBook.get_book_full_author_by_id(book_id)
                    param = self.__servRental.check_rentals_after_book_or_client_removes(type_book_or_client, book_id)
                    self.__servBook.remove_book(book_id)
                    yes_or_no = param[0]
                    rental_id = param[1]
                    rent_date = param[2]
                    client_id = param[3]
                    if yes_or_no == "yes":
                        param_2 = [rental_id, rent_date, client_id]
                    else:
                        param_2 = ["-", "-", "-"]
                    function_and_param = ["add book", [book_id, title, author], yes_or_no, param_2]
                    undo_list.append(function_and_param)
                    times_undo = times_undo + 1
                    redo_list.clear()
                    times_redo = 0
                except ValueError:
                    print("The id has to be an integer")
                except ValidError as ve:
                    print(ve)
                except RepoError as re:
                    print(re)
            elif c[0] == 'update' and c[1] == 'book' and len(c) == 2:
                try:
                    book_id = int(input("Please enter an id: "))
                    new_title = str(input("Please enter the book's new title: "))
                    new_author = str(input("Please enter the book's new author: "))
                    old_title = self.__servBook.get_book_full_title_by_id(book_id)
                    old_author = self.__servBook.get_book_full_author_by_id(book_id)
                    self.__servBook.update_book(book_id, new_title, new_author)
                    function_and_param = ["update book", [book_id, old_title, old_author, new_title, new_author]]
                    undo_list.append(function_and_param)
                    times_undo = times_undo + 1
                    redo_list.clear()
                    times_redo = 0
                except ValueError:
                    print("The id has to be an integer")
                except ValidError as ve:
                    print(ve)
                except RepoError as re:
                    print(re)
            elif c[0] == 'list' and c[1] == 'books' and len(c) == 2:
                books_list = self.__servBook.get_all_books()
                if len(books_list) == 0:
                    print("There is no book!")
                else:
                    for i in books_list:
                        print(str(i))
            elif c[0] == 'rent' and len(c) == 5:
                try:
                    rental_id = int(c[1])
                    rent_date = c[2]
                    book_id = int(c[3])
                    client_id = int(c[4])
                    self.__servRental.rent_book(rental_id, rent_date, book_id, client_id)
                    function_and_param = ["return", [rental_id, rent_date, "-", book_id, client_id]]
                    undo_list.append(function_and_param)
                    times_undo = times_undo + 1
                    redo_list.clear()
                    times_redo = 0
                    print("The book was successfully rented!")
                except ValueError:
                    print("Invalid ids!")
                except ValidError as ve:
                    print(ve)
                except RepoError as re:
                    print(re)
            elif c[0] == 'return' and len(c) == 5:
                try:
                    rental_id = int(c[1])
                    return_date = c[2]
                    book_id = int(c[3])
                    client_id = int(c[4])
                    rent_date = self.__servRental.get_the_rent_date_from_id(rental_id)
                    self.__servRental.return_book(rental_id, return_date, book_id, client_id)
                    function_and_param = ["rent", [rental_id, rent_date, return_date, book_id, client_id]]
                    undo_list.append(function_and_param)
                    times_undo = times_undo + 1
                    redo_list.clear()
                    times_redo = 0
                    print("The book was successfully returned!")
                except ServError as se:
                    print(se)
                except ValueError as vee:
                    print(vee)      # del
                    print("Invalid ids!")
                except ValidError as ve:
                    print(ve)
                except RepoError as re:
                    print(re)
            elif c[0] == 'list' and c[1] == 'rentals' and len(c) == 2:
                rentals_list = self.__servRental.get_all_rentals()
                if len(rentals_list) == 0:
                    print("There is no rental!")
                else:
                    for i in rentals_list:
                        print(str(i))
            elif c[0] == 'search' and c[1] == 'book' and c[2] == 'by' and c[3] == 'id' and len(c) == 4:
                try:
                    book_id = str(input("Please enter a part of a book's id: "))
                    book_list = self.__servBook.search_book_by_id(book_id)
                    if len(book_list) == 0:
                        print("There is no book with this id!")
                    else:
                        for i in book_list:
                            print(str(i))
                except ValueError:
                    print("Invalid id!")
                except ServError as se:
                    print(se)
                except ValidError as ve:
                    print(ve)
                except RepoError as re:
                    print(re)
            elif c[0] == 'search' and c[1] == 'book' and c[2] == 'by' and c[3] == 'title' and len(c) == 4:
                try:
                    book_title = input("Please enter a part of a title: ")
                    book_list = self.__servBook.search_book_by_title(book_title)
                    if len(book_list) == 0:
                        print("There is no book with this title!")
                    else:
                        for i in book_list:
                            print(str(i))
                except ValueError:
                    print("Invalid id!")
                except ServError as se:
                    print(se)
                except ValidError as ve:
                    print(ve)
                except RepoError as re:
                    print(re)
            elif c[0] == 'search' and c[1] == 'book' and c[2] == 'by' and c[3] == 'author' and len(c) == 4:
                try:
                    book_author = input("Please enter a part of an author's name: ")
                    book_list = self.__servBook.search_book_by_author(book_author)
                    if len(book_list) == 0:
                        print("There is no book with this author!")
                    else:
                        for i in book_list:
                            print(str(i))
                except ValueError:
                    print("Invalid id!")
                except ServError as se:
                    print(se)
                except ValidError as ve:
                    print(ve)
                except RepoError as re:
                    print(re)
            elif c[0] == 'search' and c[1] == 'client' and c[2] == 'by' and c[3] == 'id' and len(c) == 4:
                try:
                    client_id = str(input("Please enter a part of a client's id: "))
                    client_list = self.__servClient.search_client_by_id(client_id)
                    if len(client_list) == 0:
                        print("There is no client with this id!")
                    else:
                        for i in client_list:
                            print(str(i))
                except ValueError:
                    print("Invalid id!")
                except ServError as se:
                    print(se)
                except ValidError as ve:
                    print(ve)
                except RepoError as re:
                    print(re)
            elif c[0] == 'search' and c[1] == 'client' and c[2] == 'by' and c[3] == 'name' and len(c) == 4:
                try:
                    client_name = input("Please enter a part of a client's name: ")
                    client_list = self.__servClient.search_client_by_name(client_name)
                    if len(client_list) == 0:
                        print("There is no client with this name!")
                    else:
                        for i in client_list:
                            print(str(i))
                except ValueError:
                    print("Invalid id!")
                except ServError as se:
                    print(se)
                except ValidError as ve:
                    print(ve)
                except RepoError as re:
                    print(re)
            elif c[0] == 'most' and c[1] == 'rented' and c[2] == 'books' and len(c) == 3:
                try:
                    list_most_rented_books = self.__servRental.most_rented_books()
                    if len(list_most_rented_books) == 0:
                        print("No books have been rented so far!")
                    else:
                        for i in list_most_rented_books:
                            times = i[0]
                            title = i[1]
                            print("Title: " + str(title) + ", times: " + str(times))
                except ServError as se:
                    print(se)
                except ValidError as ve:
                    print(ve)
                except RepoError as re:
                    print(re)
            elif c[0] == 'most' and c[1] == 'rented' and c[2] == 'authors' and len(c) == 3:
                try:
                    list_most_rented_authors = self.__servRental.most_rented_authors()
                    if len(list_most_rented_authors) == 0:
                        print("No books have been rented so far!")
                    else:
                        for i in list_most_rented_authors:
                            times = i[0]
                            author = i[1]
                            print("Author: " + str(author) + ", times: " + str(times))
                except ServError as se:
                    print(se)
                except ValidError as ve:
                    print(ve)
                except RepoError as re:
                    print(re)
            elif c[0] == 'most' and c[1] == 'active' and c[2] == 'clients' and len(c) == 3:
                try:
                    list_most_active_clients = self.__servRental.most_active_clients()
                    if len(list_most_active_clients) == 0:
                        print("No client has returned a book so far!")
                    else:
                        for i in list_most_active_clients:
                            days = i[0]
                            name = i[1]
                            print("Name: " + str(name) + ", days: " + str(days))
                except ServError as se:
                    print(se)
                except ValidError as ve:
                    print(ve)
                except RepoError as re:
                    print(re)
            elif c[0] == 'undo' and len(c) == 1:
                if times_undo != 0:
                    function_and_param = undo_list[-1]
                    # function_and_param looks like [function,[param1,param2,...]]
                    # or [function1,[param1,param2,...],function2,[param1,param2,...]]
                    function = function_and_param[0]
                    if function == "add book":
                        param_1 = function_and_param[1]  # parameters for the add_book function
                        book_id = param_1[0]
                        title = param_1[1]
                        author = param_1[2]
                        yes_or_no = function_and_param[2]
                        param_2 = function_and_param[3]  # parameters for the rent_book function
                        rental_id = param_2[0]
                        rent_date = param_2[1]
                        client_id = param_2[2]
                        try:
                            self.__servBook.add_book(book_id, title, author)
                            function_and_param = ["remove book", [book_id, title, author], yes_or_no, param_2]
                            redo_list.append(function_and_param)
                        except ValueError:
                            print("The id has to be an integer")
                        except ValidError as ve:
                            print(ve)
                        except RepoError as re:
                            print(re)
                        if yes_or_no == "yes":  # if it's yes then it was rented before the removal
                            try:
                                self.__servRental.rent_book(rental_id, rent_date, book_id, client_id)

                            except ValueError:
                                print("Invalid ids!")
                            except ValidError as ve:
                                print(ve)
                            except RepoError as re:
                                print(re)
                    elif function == "update book":
                        param = function_and_param[1]  # parameters for the update_book function
                        book_id = param[0]
                        old_title = param[1]
                        old_author = param[2]
                        new_title = param[3]
                        new_author = param[4]
                        try:
                            self.__servBook.update_book(book_id, old_title, old_author)
                            function_and_param = ["update book",
                                                  [book_id, old_title, old_author, new_title, new_author]]
                            redo_list.append(function_and_param)
                        except ValueError:
                            print("The id has to be an integer")
                        except ValidError as ve:
                            print(ve)
                        except RepoError as re:
                            print(re)
                    elif function == "remove book":
                        param_1 = function_and_param[1]  # parameters for the remove_book function
                        book_id = param_1[0]
                        title = param_1[1]
                        author = param_1[2]
                        yes_or_no = function_and_param[2]
                        param_2 = function_and_param[3]
                        type_book_or_client = "book"
                        try:
                            self.__servBook.remove_book(book_id)
                        except ValueError:
                            print("The id has to be an integer")
                        except ValidError as ve:
                            print(ve)
                        except RepoError as re:
                            print(re)
                        try:
                            self.__servRental.undo_check_rentals_after_book_or_client_removes(type_book_or_client, book_id)
                            function_and_param = ["add book", [book_id, title, author], yes_or_no, param_2]
                            redo_list.append(function_and_param)
                        except ValueError:
                            print("The id has to be an integer")
                        except ValidError as ve:
                            print(ve)
                        except RepoError as re:
                            print(re)
                    elif function == "add client":
                        param_1 = function_and_param[1]  # parameters for the add_client function
                        client_id = param_1[0]
                        name = param_1[1]
                        yes_or_no = function_and_param[2]
                        param_2 = function_and_param[3]  # parameters for the rent_book function
                        rental_id = param_2[0]
                        rent_date = param_2[1]
                        book_id = param_2[2]
                        try:
                            self.__servClient.add_client(client_id, name)
                            function_and_param = ["remove client", [client_id, name], yes_or_no, param_2]
                            redo_list.append(function_and_param)
                        except ValueError:
                            print("The id has to be an integer")
                        except ValidError as ve:
                            print(ve)
                        except RepoError as re:
                            print(re)
                        if yes_or_no == "yes":  # if it's yes then it was rented before the removal
                            try:
                                self.__servRental.rent_book(rental_id, rent_date, book_id, client_id)
                            except ValueError:
                                print("Invalid ids!")
                            except ValidError as ve:
                                print(ve)
                            except RepoError as re:
                                print(re)
                    elif function == "update client":
                        param = function_and_param[1]  # parameters for the update_client function
                        client_id = param[0]
                        old_name = param[1]
                        new_name = param[2]
                        try:
                            self.__servClient.update_client(client_id, old_name)
                            function_and_param = ["update client", [client_id, old_name, new_name]]
                            redo_list.append(function_and_param)
                        except ValueError:
                            print("The id has to be an integer")
                        except ValidError as ve:
                            print(ve)
                        except RepoError as re:
                            print(re)
                    elif function == "remove client":
                        param = function_and_param[1]  # parameters for the remove_client function
                        client_id = param[0]
                        name = param[1]
                        yes_or_no = function_and_param[2]
                        param_2 = function_and_param[3]
                        type_book_or_client = "client"
                        try:
                            self.__servRental.undo_check_rentals_after_book_or_client_removes(type_book_or_client, client_id)
                            function_and_param = ["add client", [client_id, name], yes_or_no, param_2]
                            redo_list.append(function_and_param)
                        except ValueError:
                            print("The id has to be an integer")
                        except ValidError as ve:
                            print(ve)
                        except RepoError as re:
                            print(re)
                        try:
                            self.__servClient.remove_client(client_id)
                        except ValueError:
                            print("The id has to be an integer")
                        except ValidError as ve:
                            print(ve)
                        except RepoError as re:
                            print(re)
                    elif function == "rent":
                        param = function_and_param[1]  # parameters for the rent_book function
                        rental_id = param[0]
                        rent_date = param[1]
                        return_date = param[2]
                        book_id = param[3]
                        client_id = param[4]
                        try:
                            self.__servRental.rent_book(rental_id, rent_date, book_id, client_id)
                            function_and_param = ["return", [rental_id, rent_date, return_date, book_id, client_id]]
                            redo_list.append(function_and_param)
                            print("The book was successfully rented!")
                        except ValueError:
                            print("Invalid ids!")
                        except ValidError as ve:
                            print(ve)
                        except RepoError as re:
                            print(re)
                    elif function == "return":
                        param = function_and_param[1]  # parameters for the undo_rent function
                        rental_id = param[0]
                        rent_date = param[1]
                        return_date = param[2]
                        book_id = param[3]
                        client_id = param[4]
                        try:
                            self.__servRental.undo_rent(rental_id, book_id, client_id)
                            function_and_param = ["rent", [rental_id, rent_date, return_date, book_id, client_id]]
                            redo_list.append(function_and_param)
                            print("The book was successfully returned!")
                        except ServError as se:
                            print(se)
                        except ValidError as ve:
                            print(ve)
                        except RepoError as re:
                            print(re)
                        except ValueError as vee:
                            print(vee)  # del
                            print("Invalid ids!")
                    else:
                        print("Something is wrong with the undo function!!!!!!!!")
                    undo_list.pop()
                    times_undo = times_undo - 1
                    times_redo = times_redo + 1
                else:
                    print("No more undos!")
            elif c[0] == 'redo' and len(c) == 1:
                if times_redo != 0:
                    try:
                        function_and_param = redo_list[-1]
                    except IndexError as ie:
                        print(ie)
                        return
                    # function_and_param looks like [function,[param1,param2,...]]
                    # or [function1,[param1,param2,...],function2,[param1,param2,...]]
                    function = function_and_param[0]
                    if function == "add book":
                        param_1 = function_and_param[1]  # parameters for the add_book function
                        book_id = param_1[0]
                        title = param_1[1]
                        author = param_1[2]
                        yes_or_no = function_and_param[2]  # parameters for the rent_book function
                        param_2 = function_and_param[3]
                        try:
                            self.__servBook.add_book(book_id, title, author)
                            function_and_param = ["remove book", [book_id, title, author], yes_or_no, param_2]
                            undo_list.append(function_and_param)
                        except ValueError:
                            print("The id has to be an integer")
                        except ValidError as ve:
                            print(ve)
                        except RepoError as re:
                            print(re)
                        if yes_or_no == "yes":  # if it's yes then it was rented before the removal
                            rental_id = param_2[0]
                            rent_date = param_2[1]
                            client_id = param_2[2]
                            try:
                                self.__servRental.rent_book(rental_id, rent_date, book_id, client_id)
                            except ValueError:
                                print("Invalid ids!")
                            except ValidError as ve:
                                print(ve)
                            except RepoError as re:
                                print(re)
                    elif function == "update book":
                        param = function_and_param[1]  # parameters for the update_book function
                        book_id = param[0]
                        old_title = param[1]
                        old_author = param[2]
                        new_title = param[3]
                        new_author = param[4]
                        try:
                            self.__servBook.update_book(book_id, old_title, old_author)
                            function_and_param = ["update book",
                                                  [book_id, old_title, old_author, new_title, new_author]]
                            undo_list.append(function_and_param)
                        except ValueError:
                            print("The id has to be an integer")
                        except ValidError as ve:
                            print(ve)
                        except RepoError as re:
                            print(re)
                    elif function == "remove book":
                        param_1 = function_and_param[1]  # parameters for the remove_book function
                        book_id = param_1[0]
                        title = param_1[1]
                        author = param_1[2]
                        yes_or_no = function_and_param[2]
                        param_2 = function_and_param[3]
                        type_book_or_client = "book"
                        try:
                            self.__servRental.undo_check_rentals_after_book_or_client_removes(type_book_or_client, book_id)
                            function_and_param = ["add book", [book_id, title, author], yes_or_no, param_2]
                            undo_list.append(function_and_param)
                        except ValueError:
                            print("The id has to be an integer")
                        except ValidError as ve:
                            print(ve)
                        except RepoError as re:
                            print(re)
                        try:
                            self.__servBook.remove_book(book_id)
                        except ValueError:
                            print("The id has to be an integer")
                        except ValidError as ve:
                            print(ve)
                        except RepoError as re:
                            print(re)
                    elif function == "add client":
                        param_1 = function_and_param[1]  # parameters for the add_client function
                        client_id = param_1[0]
                        name = param_1[1]
                        yes_or_no = function_and_param[2]
                        param_2 = function_and_param[3]  # parameters for the rent_book function
                        try:
                            self.__servClient.add_client(client_id, name)
                            function_and_param = ["remove client", [client_id, name], yes_or_no, param_2]
                            undo_list.append(function_and_param)
                        except ValueError:
                            print("The id has to be an integer")
                        except ValidError as ve:
                            print(ve)
                        except RepoError as re:
                            print(re)
                        if yes_or_no == "yes":  # if it's yes then it was rented before the removal
                            rental_id = param_2[0]
                            rent_date = param_2[1]
                            book_id = param_2[2]
                            try:
                                self.__servRental.rent_book(rental_id, rent_date, book_id, client_id)
                            except ValueError:
                                print("Invalid ids!")
                            except ValidError as ve:
                                print(ve)
                            except RepoError as re:
                                print(re)
                    elif function == "update client":
                        param = function_and_param[1]  # parameters for the update_client function
                        client_id = param[0]
                        old_name = param[1]
                        new_name = param[2]
                        try:
                            self.__servClient.update_client(client_id, new_name)
                            function_and_param = ["update client", [client_id, old_name, new_name]]
                            undo_list.append(function_and_param)
                        except ValueError:
                            print("The id has to be an integer")
                        except ValidError as ve:
                            print(ve)
                        except RepoError as re:
                            print(re)
                    elif function == "remove client":
                        param = function_and_param[1]  # parameters for the remove_client function
                        client_id = param[0]
                        name = param[1]
                        yes_or_no = function_and_param[2]
                        param_2 = function_and_param[3]
                        type_book_or_client = "client"
                        try:
                            self.__servRental.undo_check_rentals_after_book_or_client_removes(type_book_or_client, client_id)
                        except ValueError:
                            print("The id has to be an integer")
                        except ValidError as ve:
                            print(ve)
                        except RepoError as re:
                            print(re)
                        try:
                            self.__servClient.remove_client(client_id)
                            function_and_param = ["add client", [client_id, name], yes_or_no, param_2]
                            undo_list.append(function_and_param)
                        except ValueError:
                            print("The id has to be an integer")
                        except ValidError as ve:
                            print(ve)
                        except RepoError as re:
                            print(re)
                    elif function == "rent":
                        param = function_and_param[1]  # parameters for the rent_book function
                        rental_id = param[0]
                        rent_date = param[1]
                        return_date = param[2]
                        book_id = param[3]
                        client_id = param[4]
                        try:
                            self.__servRental.rent_book(rental_id, rent_date, book_id, client_id)
                            function_and_param = ["return", [rental_id, rent_date, return_date, book_id, client_id]]
                            undo_list.append(function_and_param)
                            print("The book was successfully rented!")
                        except ValueError:
                            print("Invalid ids!")
                        except ValidError as ve:
                            print(ve)
                        except RepoError as re:
                            print(re)
                    elif function == "return":
                        param = function_and_param[1]  # parameters for the return_book function
                        rental_id = param[0]
                        rent_date = param[1]
                        return_date = param[2]
                        book_id = param[3]
                        client_id = param[4]
                        try:
                            self.__servRental.return_book(rental_id, return_date, book_id, client_id)
                            function_and_param = ["rent", [rental_id, rent_date, return_date, book_id, client_id]]
                            undo_list.append(function_and_param)
                            print("The book was successfully returned!")
                        except ServError as se:
                            print(se)
                        except ValidError as ve:
                            print(ve)
                        except RepoError as re:
                            print(re)
                    redo_list.pop()
                    times_redo = times_redo - 1
                    times_undo = times_undo + 1
                else:
                    print("No more redos!")
            else:
                print("Invalid command!")

    def generate_book_list(self):
        titles = ["Such a Fun Age", "99 Nights in Logar", "The Dreamers", "Followers", "The Glass Hotel", "The Mirror & the Light", "Long Bright River", "Uncanny Valley", "The Ballad of Songbirds and Snakes", "The Beauty of Your Face", "Murder on the Orient Express", "The Hound of the Baskervilles", "A Study in Scarlet", "The Sign of the Four", "Harry Potter and the Philosopher's Stone", "A Long Petal of the Sea"]
        authors = ["Kiley Reid", "Jamil Jan Kochai", "Karen Thompson Walker", "Megan Angelo", "Emily St. John Mandel", "Hillary Mantel", "Liz Moore", "Anna Weiner", "Suzanne Collins", "Sahar Mustafah", "Agatha Christie", "Arthur Conan Doyle", "Arthur Conan Doyle", "Arthur Conan Doyle", "J. K. Rowling", "Isabel Allende"]
        for i in range(0, 12):
            try:
                book_id = random.randint(1, 1000)
                title = random.choice(titles)
                index = titles.index(title)
                author = authors[index]
                self.__servBook.add_book(book_id, title, author)
            except ValueError:
                print("the id has to be an integer")
            except ValidError:
                print("this book is not valid")
            except RepoError:
                pass

    def generate_client_list(self):
        names = ["Petre Miriam", "Anghelescu Valentina", "Popa Maria", "Marian Daria", "Trofin Marius", "Bota David",
                 "Serea Alexandru", "Cobeniuc Cristina", "Dumitru Florin", "Iancu Octavia", "Petre Corina",
                 "Simion David", "Mihailean Ovidiu", "Nica Darius", "Alexandru Diana", "Floroian Corneliu"]
        for i in range(0, 14):
            try:
                client_id = random.randint(1, 100)
                name = random.choice(names)
                index = names.index(name)
                names.pop(index)
                self.__servClient.add_client(client_id, name)
            except ValueError:
                print("the id has to be an integer")
            except ValidError:
                print("the client is not valid")
            except RepoError:
                pass


if __name__ == '__main__':
    validBook = ValidatorBook()
    validClient = ValidatorClient()
    validRental = ValidatorRental()
    input_type = get_type()
    if input_type == "inmemory":
        repoBook = RepoBook()
        repoClient = RepoClient()
        repoRental = RepoRental()
    elif input_type == "textfile":
        repoBook = BooksFile(get_file_for_books())
        repoClient = ClientsFile(get_file_for_clients())
        repoRental = RentalsFile(get_file_for_rentals())
    elif input_type == "binaryfile":
        repoBook = BooksBinary(get_file_for_books())
        repoClient = ClientsBinary(get_file_for_clients())
        repoRental = RentalsBinary(get_file_for_rentals())
    else:
        sys.exit("Something is wrong with the repos.")
    servBook = ServiceBook(validBook, repoBook)
    servClient = ServiceClient(validClient, repoClient)
    servRental = ServiceRental(validRental, repoRental, repoBook, repoClient)
    tests = Tests(servBook, servClient, repoBook, repoClient, validBook, validClient)
    tests.run_all_tests()
    tests_gnome_sort_and_filter = GnomeSortAndFilterTests()
    tests_gnome_sort_and_filter.test_gnome_sort()
    tests_gnome_sort_and_filter.test_filter()
    tests_iterable_data_structure = IterableDataStructureTests()
    tests_iterable_data_structure.test_iterable_data_structure()
    ui = UI(servBook, servClient, servRental)
    ui.start()
