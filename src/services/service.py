from validation.validators import ServError
from domain.entities import Book, Client, Rental
from domain.a10module import gnome_sort


class ServiceBook(object):

    def __init__(self, validBook, repoBook):
        self.__repoBook = repoBook
        self.__validBook = validBook

    def add_book(self, book_id, title, author):
        """
        Adds a book to the library(book_list)
        :param book_id: the id of the book we want to add
        :param title: the title of the book we want to add
        :param author: the author of the book we want to add
        """
        book = Book(book_id, title, author)
        self.__validBook.validate_book(book)
        self.__repoBook.add(book)

    def remove_book(self, book_id):
        """
        Removes a book from the library(book_list)
        :param book_id: the id of the book we want to remove
        :return:
        """
        book = self.__repoBook.get_book_by_id(book_id)
        self.__repoBook.remove(book)

    def update_book(self, book_id, new_title, new_author):
        """
        It changes the title and author of the book with the given id
        :param book_id: the id of the book we want to update
        :param new_title: the new title of the book
        :param new_author: the new author of the book
        """
        book = self.__repoBook.get_book_by_id(book_id)
        self.__repoBook.update(book, new_title, new_author)
        self.__validBook.validate_book(book)

    def search_book_by_id(self, book_id):
        """
        It looks for the book that has the given id
        :param book_id: the given id
        :return:the book with the given id if there is one otherwise nothing
        """
        book_by_id_list = self.__repoBook.get_book_by_partial_id(book_id)
        return book_by_id_list

    def search_book_by_title(self, book_title):
        """
        It looks for the book that has the given title
        :param book_title: the given title
        :return:the book with the given title if there is one otherwise nothing
        """
        book_by_title_list = self.__repoBook.get_book_by_partial_title(book_title)
        return book_by_title_list

    def search_book_by_author(self, book_author):
        """
        It looks for the book that has the given author
        :param book_author: the given author
        :return:the book with the given author if there is one otherwise nothing
        """
        book_by_author_list = self.__repoBook.get_book_by_partial_author(book_author)
        return book_by_author_list

    def get_book_full_title_by_id(self, book_id):
        """
               It looks for the book that has the given id
               :param book_id: the given id
               :return:the book with the given id if there is one otherwise nothing
               """
        title = self.__repoBook.get_book_title_by_id(book_id)
        return title

    def get_book_full_author_by_id(self, book_id):
        """
               It looks for the client that has the given id
               :param book_id: the given id
               :return:the book with the given id if there is one otherwise nothing
               """
        author = self.__repoBook.get_book_author_by_id(book_id)
        return author

    def get_all_books(self):
        return self.__repoBook.get_all()


class ServiceClient(object):

    def __init__(self, validClient, repoClient):
        self.__repoClient = repoClient
        self.__validClient = validClient

    def add_client(self, client_id, name):
        """
        Adds a client to the client_list
        :param client_id: the id of the client we want to add
        :param name: the name of the client we want to add
        """
        client = Client(client_id, name)
        self.__validClient.validate_client(client)
        self.__repoClient.add(client)

    def remove_client(self, client_id):
        """
        Removes a client from the client_list
        :param client_id:the id of the book we want to remove
        """
        client = self.__repoClient.get_client_by_id(client_id)
        self.__repoClient.remove(client)

    def update_client(self, client_id, new_name):
        """
        It changes the name of the client with the given id
        :param client_id: the id of the client we want to update
        :param new_name: the new name
        """
        client = self.__repoClient.get_client_by_id(client_id)
        self.__repoClient.update(client, new_name)
        self.__validClient.validate_client(client)

    def search_client_by_id(self, client_id):
        """
        It looks for the client that has the given id
        :param client_id: the given id
        :return:the client with the given id if there is one otherwise nothing
        """
        client_by_id_list = self.__repoClient.get_client_by_partial_id(client_id)
        return client_by_id_list

    def search_client_by_name(self, client_name):
        """
        It looks for the client that has the given name
        :param client_name:
        :return:the client with the given name if there is one otherwise nothing
        """
        client_by_name_list = self.__repoClient.get_client_by_partial_name(client_name)
        return client_by_name_list

    def get_client_full_name_by_id(self, client_id):
        """
        It looks for the client that has the given id
        :param client_id: the given id
        :return:the client with the given id if there is one otherwise nothing
        """
        name = self.__repoClient.get_client_name_by_id(client_id)
        return name

    def get_all_clients(self):
        return self.__repoClient.get_all()


class ServiceRental(object):
    def __init__(self, validRental, repoRental, repoBook, repoClient):
        self.__validRental = validRental
        self.__repoRental = repoRental
        self.__repoBook = repoBook
        self.__repoClient = repoClient
        self.__rented_books_ids_at_the_moment = []
        self.__rented_clients_ids_at_the_moment = []
        for rent in self.__repoRental.get_all():
            b_id = self.__repoRental.get_book_id_by_rent(rent)
            self.__rented_books_ids_at_the_moment.append(b_id)
        for rent in self.__repoRental.get_all():
            c_id = self.__repoRental.get_client_id_by_rent(rent)
            self.__rented_clients_ids_at_the_moment.append(c_id)
        self.__most_rented_books_by_id = []
        self.__most_active_clients_by_id = []

    @staticmethod
    def leapyear(value):
        if value % 4 == 0 and value % 100 != 0:
            return True
        elif value % 4 == 0 and value % 100 == 0 and value % 400 == 0:
            return True
        else:
            return False

    def get_days(self, rent_date, return_date):
        days = 0
        nrdays = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        # add the full years between the dates
        start_date = rent_date.split(".")
        sd = int(start_date[0])
        sm = int(start_date[1])
        sy = int(start_date[2])
        end_date = return_date.split(".")
        ed = int(end_date[0])
        em = int(end_date[1])
        ey = int(end_date[2])
        if (ey - sy) >= 3:
            for i in range(sy, ey - 1):
                if self.leapyear(i) is True:
                    days = days + 366
                else:
                    days = days + 365
        elif (ey - sy) == 2:
            if self.leapyear(sy + 1) is True:
                days = 366
            else:
                days = 365
        else:  # same year or consecutive years
            days = 0
        # add the days outside the full years
        for x in range(sm, 12):
            days = days + nrdays[x]
        days = days + nrdays[sm - 1] - sd
        if self.leapyear(sy) is True and (sm == 1 or (sm == 2 and sd == 28)):
            days = days + 1
        for y in range(0, em - 1):
            days = days + nrdays[y]
        days = days + ed + 1
        # special cases
        if sd == ed and sm == em and sy == ey:
            days = 0
        if sy == ey and sm == em and sd != ed:
            days = ed - sd
        if sy == ey and sm != em and sd == ed:
            for n in range(sm - 1, em - 1):
                days = nrdays[n]
            if self.leapyear(sy) is True and sm == 2:
                days = days + 1
        if ey == sy + 1 and sm == em and sd == ed:
            if self.leapyear(sy) is True and sm == 1:
                days = 366
            else:
                days = 365
        return days

    def rent_book(self, rental_id, rent_date, book_id, client_id):
        book = self.__repoBook.get_book_by_id(book_id)
        book_list = self.__repoBook.get_all()
        if book not in book_list:
            raise ServError("This book doesn't exist!")
        client = self.__repoClient.get_client_by_id(client_id)
        client_list = self.__repoClient.get_all()
        if client not in client_list:
            raise ServError("This client doesn't exist!")

        return_date = '-'
        rental = Rental(rental_id, book_id, client_id, rent_date, return_date)
        self.__validRental.validate_rental(rental)
        self.__repoRental.add(rental)
        self.__rented_books_ids_at_the_moment.append(book_id)
        self.__rented_clients_ids_at_the_moment.append(client_id)
        length_list = len(self.__most_rented_books_by_id)
        if length_list == 0:
            title = self.__repoBook.get_book_title_by_id(book_id)
            author = self.__repoBook.get_book_author_by_id(book_id)
            new_book = [1, title, author, book_id]
            self.__most_rented_books_by_id.append(new_book)
        else:
            for i in range(0, length_list):
                id_current_book = self.__most_rented_books_by_id[i][3]
                title_current_book = self.__repoBook.get_book_title_by_id(id_current_book)
                title_rented_book = self.__repoBook.get_book_title_by_id(book_id)
                if id_current_book == book_id:
                    self.__most_rented_books_by_id[i][0] = self.__most_rented_books_by_id[i][0] + 1
                    return
                elif title_current_book == title_rented_book:
                    self.__most_rented_books_by_id[i][0] = self.__most_rented_books_by_id[i][0] + 1
                    return
            title = self.__repoBook.get_book_title_by_id(book_id)
            author = self.__repoBook.get_book_author_by_id(book_id)
            new_book = [1, title, author, book_id]
            self.__most_rented_books_by_id.append(new_book)

    def return_book(self, rental_id, return_date, book_id, client_id):
        book = self.__repoBook.get_book_by_id(book_id)
        book_list = self.__repoBook.get_all()
        if book not in book_list:
            raise ServError("This book doesn't exist!")
        client = self.__repoClient.get_client_by_id(client_id)
        client_list = self.__repoClient.get_all()
        if client not in client_list:
            raise ServError("This client doesn't exist!")
        for current_book_id in self.__rented_books_ids_at_the_moment:
            if int(current_book_id) == int(book_id):
                index_book = self.__rented_books_ids_at_the_moment.index(current_book_id)
                current_client_id = self.__rented_clients_ids_at_the_moment[index_book]
                if int(current_client_id) == int(client_id):
                    rent_date = self.__repoRental.get_rent_date_by_id(rental_id)
                    re_date = "-"
                    rental = Rental(rental_id, book_id, client_id, rent_date, re_date)
                    self.__validRental.validate_rental(rental)
                    self.__repoRental.remove(rental, book_id, client_id)
                    self.__rented_books_ids_at_the_moment.pop(index_book)
                    self.__rented_clients_ids_at_the_moment.pop(index_book)
                    length_list = len(self.__most_active_clients_by_id)
                    if length_list == 0:
                        rent_date = rental.get_rent_date()
                        days = self.get_days(rent_date, return_date)
                        name = self.__repoClient.get_client_name_by_id(client_id)
                        new_client = [days, name, client_id]
                        self.__most_active_clients_by_id.append(new_client)
                    else:
                        for i in range(0, length_list):
                            if self.__most_active_clients_by_id[i][2] == client_id:
                                rent_date = rental.get_rent_date()
                                days = self.get_days(rent_date, return_date)
                                self.__most_active_clients_by_id[i][0] = self.__most_active_clients_by_id[i][0] + days
                                return
                        rent_date = rental.get_rent_date()
                        days = self.get_days(rent_date, return_date)
                        name = self.__repoClient.get_client_name_by_id(client_id)
                        new_client = [days, name, client_id]
                        self.__most_active_clients_by_id.append(new_client)
                    return
        raise ServError("This book is not rented")

    def most_rented_books(self):
        most_rented_titles = []
        most_rented_books = self.__most_rented_books_by_id
        for i in most_rented_books:
            index_rented_book = most_rented_books.index(i)
            times = most_rented_books[index_rented_book][0]
            title = most_rented_books[index_rented_book][1]
            rented_book = [times, title]
            if len(most_rented_titles) == 0:
                most_rented_titles.append(rented_book)
            else:
                for x in most_rented_titles:
                    index_title = most_rented_titles.index(x)
                    if most_rented_titles[index_title][1] == rented_book:
                        most_rented_titles[index_title][0] += times
                        return
                most_rented_titles.append(rented_book)
        # ordered_most_rented_titles = []
        # timess_list = []
        # title_list = []
        # for rented_b in most_rented_titles:
        #     timess = rented_b[0]
        #     title = rented_b[1]
        #     timess_list.append(timess)
        #     title_list.append(title)
        # length = len(timess_list)
        # for i in range(length - 1):
        #     for j in range(0, length - i - 1):
        #         if timess_list[j] < timess_list[j + 1]:
        #             timess_list[j], timess_list[j + 1] = timess_list[j + 1], timess_list[j]
        #             title_list[j], title_list[j + 1] = title_list[j + 1], title_list[j]
        # for x in range(0, length):
        #     ordered_b = [timess_list[x], title_list[x]]
        #     ordered_most_rented_titles.append(ordered_b)
        ordered_most_rented_titles = gnome_sort(most_rented_titles, lambda x, y: x[0] > y[0])
        return ordered_most_rented_titles

    def most_rented_authors(self):
        most_rented_authors = []
        most_rented_books = self.__most_rented_books_by_id
        for i in most_rented_books:
            index_rented_book = most_rented_books.index(i)
            times = most_rented_books[index_rented_book][0]
            author = most_rented_books[index_rented_book][2]
            rented_book = [times, author]
            if len(most_rented_authors) == 0:
                most_rented_authors.append(rented_book)
            else:
                for x in most_rented_authors:
                    index_author = most_rented_authors.index(x)
                    if most_rented_authors[index_author][1] == rented_book:
                        most_rented_authors[index_author][0] += times
                        return
                most_rented_authors.append(rented_book)
        # ordered_most_rented_authors = []
        # timess_list = []
        # author_list = []
        # for rented_b in most_rented_authors:
        #     timess = rented_b[0]
        #     author = rented_b[1]
        #     timess_list.append(timess)
        #     author_list.append(author)
        # length = len(timess_list)
        # for i in range(length - 1):
        #     for j in range(0, length - i - 1):
        #         if timess_list[j] < timess_list[j + 1]:
        #             timess_list[j], timess_list[j + 1] = timess_list[j + 1], timess_list[j]
        #             author_list[j], author_list[j + 1] = author_list[j + 1], author_list[j]
        # for x in range(0, length):
        #     ordered_b = [timess_list[x], author_list[x]]
        #     ordered_most_rented_authors.append(ordered_b)
        ordered_most_rented_authors = gnome_sort(most_rented_authors, lambda x, y: x[0] > y[0])
        return ordered_most_rented_authors

    def most_active_clients(self):
        most_active_names = []
        most_active_clients = self.__most_active_clients_by_id
        for i in most_active_clients:
            index_active_client = most_active_clients.index(i)
            days = most_active_clients[index_active_client][0]
            name = most_active_clients[index_active_client][1]
            client_id = most_active_clients[index_active_client][2]
            active_client = [days, name, client_id]
            if len(most_active_names) == 0:
                most_active_names.append(active_client)
            else:
                for x in most_active_names:
                    index_name = most_active_names.index(x)
                    if most_active_names[index_name][1] == active_client[1]:
                        most_active_names[index_name][0] = most_active_names[index_name][0] + days
                        return
                most_active_names.append(active_client)
        # ordered_most_active_clients = []
        # timess_list = []
        # client_list = []
        # for active_c in most_active_clients:
        #     timess = active_c[0]
        #     client = active_c[1]
        #     timess_list.append(timess)
        #     client_list.append(client)
        # length = len(timess_list)
        # for i in range(length - 1):
        #     for j in range(0, length - i - 1):
        #         if timess_list[j] < timess_list[j + 1]:
        #             timess_list[j], timess_list[j + 1] = timess_list[j + 1], timess_list[j]
        #             client_list[j], client_list[j + 1] = client_list[j + 1], client_list[j]
        # for x in range(0, length):
        #     ordered_c = [timess_list[x], client_list[x]]
        #     ordered_most_active_clients.append(ordered_c)
        ordered_most_active_clients = gnome_sort(most_active_clients, lambda x, y: x[0] > y[0])
        return ordered_most_active_clients

    def check_rentals_after_book_or_client_removes(self, type_book_or_client, id_book_or_client):
        if type_book_or_client == "book":
            for book_id in self.__rented_books_ids_at_the_moment:
                if book_id == id_book_or_client:
                    rentals = self.__repoRental.get_all()
                    for rent in rentals:
                        book_id = self.__repoRental.get_book_id_by_rent(rent)
                        if str(id_book_or_client) == str(book_id):
                            client_id = self.__repoRental.get_client_id_by_rent(rent)
                            rental_id = self.__repoRental.get_rental_id_by_rent(rent)
                            rent_date = self.__repoRental.get_rent_date_by_id(rental_id)
                            self.__repoRental.remove(rent, book_id, client_id)
                            param = ["yes", rental_id, rent_date, client_id]
                            return param
        else:
            for client_id in self.__rented_clients_ids_at_the_moment:
                if client_id == id_book_or_client:
                    rentals = self.__repoRental.get_all()
                    for rent in rentals:
                        client_id = self.__repoRental.get_client_id_by_rent(rent)
                        if str(id_book_or_client) == str(client_id):
                            book_id = self.__repoRental.get_book_id_by_rent(rent)
                            rental_id = self.__repoRental.get_rental_id_by_rent(rent)
                            rent_date = self.__repoRental.get_rent_date_by_id(rental_id)
                            self.__repoRental.remove(rent, book_id, client_id)
                            param = ["yes", rental_id, rent_date, book_id]
                            return param
        param = ["no", "-", "-", "-"]
        return param

    def undo_rent(self, rental_id, book_id, client_id):
        book = self.__repoBook.get_book_by_id(book_id)
        book_list = self.__repoBook.get_all()
        if book not in book_list:
            raise ServError("This book doesn't exist!")
        client = self.__repoClient.get_client_by_id(client_id)
        client_list = self.__repoClient.get_all()
        if client not in client_list:
            raise ServError("This client doesn't exist!")
        for current_book_id in self.__rented_books_ids_at_the_moment:
            if int(current_book_id) == int(book_id):
                index_book = self.__rented_books_ids_at_the_moment.index(current_book_id)
                current_client_id = self.__rented_clients_ids_at_the_moment[index_book]
                if int(current_client_id) == int(client_id):
                    rent_date = self.__repoRental.get_rent_date_by_id(rental_id)
                    re_date = "-"
                    rental = Rental(rental_id, book_id, client_id, rent_date, re_date)
                    self.__validRental.validate_rental(rental)
                    self.__repoRental.remove(rental, book_id, client_id)
                    self.__rented_books_ids_at_the_moment.pop(index_book)
                    self.__rented_clients_ids_at_the_moment.pop(index_book)
                    length_list = len(self.__most_rented_books_by_id)
                    if length_list == 1:
                        id_current_book = self.__most_rented_books_by_id[0][3]
                        title_current_book = self.__repoBook.get_book_title_by_id(id_current_book)
                        title_rented_book = self.__repoBook.get_book_title_by_id(book_id)
                        if id_current_book == book_id:
                            self.__most_rented_books_by_id.pop()
                            return
                        elif title_current_book == title_rented_book:
                            self.__most_rented_books_by_id.pop()
                            return
                    elif length_list > 1:
                        for i in range(0, length_list):
                            id_current_book = self.__most_rented_books_by_id[i][3]
                            title_current_book = self.__repoBook.get_book_title_by_id(id_current_book)
                            title_rented_book = self.__repoBook.get_book_title_by_id(book_id)
                            if id_current_book == book_id:
                                self.__most_rented_books_by_id[i][0] = self.__most_rented_books_by_id[i][0] - 1
                                return
                            elif title_current_book == title_rented_book:
                                self.__most_rented_books_by_id[i][0] = self.__most_rented_books_by_id[i][0] - 1
                                return
                    else:
                        raise ServError("This rental has problems!")
        raise ServError("This book is not rented")

    def undo_check_rentals_after_book_or_client_removes(self, type_book_or_client, id_book_or_client):
        if type_book_or_client == "book":
            for book_id in self.__rented_books_ids_at_the_moment:
                if book_id == id_book_or_client:
                    rentals = self.__repoRental.get_all()
                    for rent in rentals:
                        book_id = self.__repoRental.get_book_id_by_rent(rent)
                        if str(id_book_or_client) == str(book_id):
                            client_id = self.__repoRental.get_client_id_by_rent(rent)
                            rental_id = self.__repoRental.get_rental_id_by_rent(rent)
                            rent_date = self.__repoRental.get_rent_date_by_id(rental_id)
                            self.__repoRental.remove(rent, book_id, client_id)
                            param = ["yes", rental_id, rent_date, client_id]
                            return param
        else:
            for client_id in self.__rented_clients_ids_at_the_moment:
                if client_id == id_book_or_client:
                    rentals = self.__repoRental.get_all()
                    for rent in rentals:
                        client_id = self.__repoRental.get_client_id_by_rent(rent)
                        if str(id_book_or_client) == str(client_id):
                            book_id = self.__repoRental.get_book_id_by_rent(rent)
                            rental_id = self.__repoRental.get_rental_id_by_rent(rent)
                            rent_date = self.__repoRental.get_rent_date_by_id(rental_id)
                            self.__repoRental.remove(rent, book_id, client_id)
                            param = ["yes", rental_id, rent_date, book_id]
                            return param
        param = ["no", "-", "-", "-"]
        return param

    def get_the_rent_date_from_id(self, rental_id):
        rent_date = self.__repoRental.get_rent_date_by_id(rental_id)
        return rent_date

    def get_all_rentals(self):
        return self.__repoRental.get_all()
