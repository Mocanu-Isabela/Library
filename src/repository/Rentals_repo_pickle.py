from validation.validators import RepoError
import pickle
import os


class RentalsBinary(object):
    def __init__(self, file_name):  # file_name='Rentals.pickle'
        self.file_name = file_name
        self.rentals = []
        self.rented_book_ids = []
        self.read_from_binary_file()
        for rent in self.rentals:
            b_id = rent.get_book_id_from_rent()
            self.rented_book_ids.append(b_id)

    def read_from_binary_file(self):
        if os.path.getsize(self.file_name) > 0:
            with open(self.file_name, "rb") as file:
                try:
                    while 1:
                        repo = pickle.load(file)
                        self.rentals.append(repo)
                except EOFError:
                    return []
                except IOError as ioe:
                    raise IOError(ioe)
            return repo

    def write_in_binary_file(self, rents):
        # ["rental_id", "book_id", "client_id", "rent_date", "return_date"]
        with open(self.file_name, "wb") as file:
            for rent in rents:
                pickle.dump(rent, file)
        file.close()

    def add(self, rent):
        for rent in self.rentals:
            b_id = rent.get_book_id_from_rent()
            self.rented_book_ids.append(b_id)
        check_book_id = rent.get_book_id_from_rent()
        for current_rent in self.rentals:
            if int(rent.get_rental_id()) == int(current_rent.get_rental_id()):
                raise RepoError("This rental id already exists!")
        for current_book_id in self.rented_book_ids:
            if int(current_book_id) == int(check_book_id):
                raise RepoError("This book is rented at the moment!")
        self.rentals.append(rent)
        self.write_in_binary_file(self.rentals)

    def remove(self, rent, book_id, client_id):
        check_book_id = int(rent.get_book_id_from_rent())
        check_client_id = int(rent.get_client_id_from_rent())
        if int(book_id) == int(check_book_id) and int(client_id) == int(check_client_id):
            for current_rent in self.rentals:
                if str(current_rent) == str(rent):
                    index = self.rentals.index(current_rent)
                    self.rentals.pop(index)
                    self.write_in_binary_file(self.rentals)
                    return
        raise RepoError("This rent doesn't exist!")

    def get_all(self):
        return self.rentals[:]

    def get_rent_date_by_id(self, rental_id):
        for rent in self.rentals:
            if int(rent.get_rental_id())==int(rental_id):
                date=rent.get_rent_date()
                return date
        raise RepoError("This rental id doesn't exist!")

    def get_client_id_by_rent(self, rent):
        return rent.get_client_id_from_rent()

    def get_book_id_by_rent(self, rent):
        return rent.get_book_id_from_rent()

    def get_rental_id_by_rent(self, rent):
        return rent.get_rental_id()
