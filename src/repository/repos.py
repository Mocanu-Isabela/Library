from validation.validators import RepoError
from domain.a10module import IterableDataStructure, filter_function


class RepoBook(object):

    def __init__(self):
        self.__book_list = IterableDataStructure()

    def add(self, book):
        """
        Adds a book to the library(book_list)
        :param book: the book that we want to add
        :return: a RepoError if there is one otherwise nothing
        """
        if book in self.__book_list:
            raise RepoError("This book already exists!")
        self.__book_list.append(book)

    def remove(self, book):
        """
        Removes a book from the library(book_list)
        :param book: the book that we want to remove
        :return: a RepoError if there is one otherwise nothing
        """
        if book not in self.__book_list:
            raise RepoError("This book doesn't exist!")
        self.__book_list.pop(book)

    def update(self, book, new_title, new_author):
        """
        It changes the title and author of the given book
        :param book: the book whose title and author we want to change
        :param new_title: the new title
        :param new_author: the new author
        :return: a RepoError if there is one otherwise nothing
        """
        if book not in self.__book_list:
            raise RepoError("This book doesn't exist!")
        book.set_title(new_title)
        book.set_author(new_author)

    def get_all(self):
        """
        It gives a shallow copy of the book list
        :return: a shallow copy of the book list
        """
        return self.__book_list[:]

    def get_book_by_id(self, book_id):
        """
        It gives the book that has the given id
        :param book_id: the id of the book we need
        :return: the book with the given id or a RepoError if there is one
        """
        filtered_list = filter_function(self.__book_list, lambda x: str(book_id) == str(x.get_book_id()))
        if len(filtered_list) == 0:
            raise RepoError("This book doesn't exist!")
        return filtered_list[0]

    def get_book_by_partial_id(self, book_id):
        """
        It gives the books that contain the given part of id
        :param book_id: the part of the id
        :return: the book with the given id or a RepoError if there is one
        """
        filtered_list = filter_function(self.__book_list, lambda x: str(book_id) in str(x.get_book_id()))
        if len(filtered_list) == 0:
            raise RepoError("There is no book with this id!")
        return filtered_list

    def get_book_by_partial_title(self, book_title):
        """
        It gives the books that contain the given part of title
        :param book_title: the part of the title
        :return: the book with the given title or a RepoError if there is one
        """

        filtered_list = filter_function(self.__book_list, lambda x: str(book_title) in str(x.get_title()))
        if len(filtered_list) == 0:
            raise RepoError("There is no book with this title!")
        return filtered_list

    def get_book_by_partial_author(self, book_author):
        """
        It gives the books that contain the given part of author
        :param book_author: the part of the author
        :return: the book with the given author or a RepoError if there is one
        """

        filtered_list = filter_function(self.__book_list, lambda x: str(book_author) in str(x.get_author()))
        if len(filtered_list) == 0:
            raise RepoError("There is no book with this author!")
        return filtered_list

    def get_book_title_by_id(self, book_id):
        for current_book in self.__book_list:
            if int(current_book.get_book_id()) == int(book_id):
                title = current_book.get_title()
                return title
        raise RepoError("This book doesn't exist!")

    def get_book_author_by_id(self, book_id):
        for current_book in self.__book_list:
            if int(current_book.get_book_id()) == int(book_id):
                author = current_book.get_author()
                return author
        raise RepoError("This book doesn't exist!")


class RepoClient(object):

    def __init__(self):
        self.__client_list = IterableDataStructure()

    def add(self, client):
        """
        Adds a client to the client_list
        :param client: the client we want to add
        :return: a RepoError if there is one otherwise nothing
        """
        for current_client in self.__client_list:
            if client.get_client_id() == current_client.get_client_id():
                raise RepoError("This client already exists!")
        self.__client_list.append(client)

    def remove(self, client):
        """
        Removes a client from the client_list
        :param client: the client we want to remove
        :return: a RepoError if there is one otherwise nothing
        """
        if client not in self.__client_list:
            raise RepoError("This client doesn't exist!")
        self.__client_list.pop(client)

    def update(self, client, new_name):
        """
        It changes the name of the client with the given id
        :param client: the client whose name we want to change
        :param new_name: the new name
        :return: a RepoError if there is one otherwise nothing
        """
        if client not in self.__client_list:
            raise RepoError("This client doesn't exist!")
        client.set_name(new_name)

    def get_all(self):
        """
        It gives a shallow copy of the client list
        :return: a shallow copy of the client list
        """
        return self.__client_list[:]

    def get_client_by_id(self, client_id):
        """
        It gives the book that has the given id
        :param client_id: the id of the client we need
        :return: the client with the given id
        """
        filtered_list = filter_function(self.__client_list, lambda x: str(client_id) == str(x.get_client_id()))
        if len(filtered_list) == 0:
            raise RepoError("This client doesn't exist!")
        return filtered_list[0]

    def get_client_by_partial_id(self, client_id):
        """
        It gives the clients that contain the given part of id
        :param client_id: the part of the id
        :return: the client with the given id or a RepoError if there is one
        """
        filtered_list = filter_function(self.__client_list, lambda x: str(client_id) in str(x.get_client_id()))
        if len(filtered_list) == 0:
            raise RepoError("There is no client with this id!")
        return filtered_list

    def get_client_by_partial_name(self, client_name):
        """
        It gives the clients that contain the given part of name
        :param client_name: the part of the name
        :return: the client with the given name or a RepoError if there is one
        """
        filtered_list = filter_function(self.__client_list, lambda x: str(client_name) in str(x.get_name()))
        if len(filtered_list) == 0:
            raise RepoError("There is no client with this name!")
        return filtered_list

    def get_client_name_by_id(self, client_id):
        for current_client in self.__client_list:
            if int(current_client.get_client_id()) == int(client_id):
                name = current_client.get_name()
                return name
        raise RepoError("This client doesn't exist!")


class RepoRental(object):

    def __init__(self):
        self.__rental_list = IterableDataStructure()
        self.__rented_books_ids = IterableDataStructure()

    def add(self, rental):
        check_book_id = rental.get_book_id_from_rent()
        for current_rent in self.__rental_list:
            if int(rental.get_rental_id()) == int(current_rent.get_rental_id()):
                raise RepoError("This rental id already exists!")
        for current_book_id in self.__rented_books_ids:
            if int(current_book_id) == int(check_book_id):
                raise RepoError("This book is rented at the moment!")
        self.__rental_list.append(rental)
        self.__rented_books_ids.append(check_book_id)

    def remove(self, rental, book_id, client_id):
        check_book_id = int(rental.get_book_id_from_rent())
        check_client_id = int(rental.get_client_id_from_rent())
        if int(book_id) == int(check_book_id) and int(client_id) == int(check_client_id):
            for current_rent in self.__rental_list:
                if str(current_rent) == str(rental):
                    # for i in self.__rental_list:   #
                    #     print(i)    #
                    # print(rental)  #
                    self.__rental_list.pop(rental)
                    self.__rented_books_ids.pop(book_id)
                    return
        raise RepoError("This rent doesn't exist!")

    def get_all(self):
        return self.__rental_list[:]

    def get_rent_date_by_id(self, rental_id):
        for rent in self.__rental_list:
            if int(rent.get_rental_id()) == int(rental_id):
                date = rent.get_rent_date()
                return date
        raise RepoError("This rental id doesn't exist!")

    def get_client_id_by_rent(self, rent):
        return rent.get_client_id_from_rent()

    def get_book_id_by_rent(self, rent):
        return rent.get_book_id_from_rent()

    def get_rental_id_by_rent(self, rent):
        return rent.get_rental_id()
