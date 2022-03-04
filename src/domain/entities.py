class Book:
    def __init__(self, book_id, title, author):
        self.__book_id = book_id
        self.__title = title
        self.__author = author

    def get_book_id(self):
        return self.__book_id

    def get_title(self):
        return self.__title

    def get_author(self):
        return self.__author

    def set_title(self, value):
        self.__title = value

    def set_author(self, value):
        self.__author = value

    def __eq__(self, other):
        return self.__book_id == other.__book_id

    def __str__(self):
        return "id: "+str(self.__book_id)+" - "+str(self.__title)+" by "+str(self.__author)


class Client:
    def __init__(self, client_id, name):
        self.__client_id = client_id
        self.__name = name

    def get_client_id(self):
        return self.__client_id

    def get_name(self):
        return self.__name

    def set_name(self, value):
        self.__name = value

    def __eq__(self, other):
        return self.__client_id == other.__client_id

    def __str__(self):
        return "id "+str(self.__client_id)+" "+str(self.__name)


class Rental:
    def __init__(self, rental_id, book_id, client_id, rent_date, return_date):
        self.__rental_id = rental_id
        self.__book_id = book_id
        self.__client_id = client_id
        self.__rent_date = rent_date
        self.__return_date = return_date

    def get_rental_id(self):
        return self.__rental_id

    def get_book_id_from_rent(self):
        return self.__book_id

    def get_client_id_from_rent(self):
        return self.__client_id

    def get_rent_date(self):
        return self.__rent_date

    def get_return_date(self):
        return self.__return_date

    def __str__(self):
        return "rental id-"+str(self.__rental_id)+", book id-"+str(self.__book_id)+", client id-"+str(self.__client_id)+", rented on:"+str(self.__rent_date)+" and returned on:"+str(self.__return_date)
