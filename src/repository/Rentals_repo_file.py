from domain.entities import Rental
from validation.validators import RepoError


class RentalsFile(object):
    def __init__(self, file_name):  # file_name='Rentals.txt'
        self.file_name = file_name

    def read_from_text_file(self):
        with open(self.file_name, "rt") as file:
            rentals=[]
            lines = file.readlines()
            for line in lines:
                if len(line) > 1:
                    line = line[:len(line) - 1].split(';')
                    # form of rent: rental id-3, book id-393, client id-8, rented on:3.2.2005 and returned on:-
                    rentals.append(Rental(int(line[0]), int(line[1]), int(line[2]), line[3], line[4]))
        file.close()
        return rentals

    def append_in_text_file(self, rent):
        with open(self.file_name, "at") as file:
            file.write(str(rent.get_rental_id()) + ";" + str(rent.get_book_id_from_rent()) + ";" + str(rent.get_client_id_from_rent()) + ";" + rent.get_rent_date() + ";" + rent.get_return_date() + '\n')
        file.close()

    def write_in_text_file(self, rents):
        with open(self.file_name, "wt") as file:
            for rent in rents:
                file.write(str(rent.get_rental_id()) + ";" + str(rent.get_book_id_from_rent()) + ";" + str(rent.get_client_id_from_rent()) + ";" + rent.get_rent_date() + ";" + rent.get_return_date() + '\n')
        file.close()

    def add(self, rent):
        rentals = self.read_from_text_file()
        rented_book_ids = []
        for current_rent in rentals:
            b_id = current_rent.get_book_id_from_rent()
            rented_book_ids.append(b_id)
            print(rent)                                # del
        print("0123456789")                            # del
        check_book_id = rent.get_book_id_from_rent()
        for current_rent in rentals:
            print(current_rent)                         # del
            if int(rent.get_rental_id()) == int(current_rent.get_rental_id()):
                print(int(rent.get_rental_id()))
                print(int(current_rent.get_rental_id()))
                raise RepoError("This rental id already exists!")
        for current_book_id in rented_book_ids:
            if int(current_book_id) == int(check_book_id):
                raise RepoError("This book is rented at the moment!")
        self.append_in_text_file(rent)

    def remove(self, rent, book_id, client_id):
        rentals = self.read_from_text_file()
        check_book_id = int(rent.get_book_id_from_rent())
        check_client_id = int(rent.get_client_id_from_rent())
        if int(book_id) == int(check_book_id) and int(client_id) == int(check_client_id):
            for current_rent in rentals:
                if str(current_rent) == str(rent):
                    index = rentals.index(current_rent)
                    rentals.pop(index)
                    self.write_in_text_file(rentals)
                    return
        raise RepoError("This rent doesn't exist!")

    def get_all(self):
        rentals = self.read_from_text_file()
        return rentals[:]

    def get_rent_date_by_id(self, rental_id):
        rentals = self.read_from_text_file()
        for rent in rentals:
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
