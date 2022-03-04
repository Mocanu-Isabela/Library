class ValidatorBook(object):

    def __init__(self):
        pass

    def validate_book(self, book):
        errors=""
        if int(book.get_book_id()) < 0:
            errors += "The id has to be a positive integer!\n"
        if len(errors) > 0:
            raise ValidError(errors)


class ValidatorClient(object):

    def __init__(self):
        pass

    def validate_client(self, client):
        errors = ""
        if int(client.get_client_id()) < 0:
            errors += "The id has to be a positive integer!\n"
        if len(errors) > 0:
            raise ValidError(errors)


class ValidatorRental(object):

    def __init__(self):
        pass

    def validate_rental(self, rental):
        errors=""
        start_date = rental.get_rent_date().split(".")
        if len(start_date)!=3:
            errors += "The dates are wrong!\n"
        else:
            sd = int(start_date[0])
            sm = int(start_date[1])
            sy = int(start_date[2])
            if int(rental.get_rental_id()) < 0:
                errors += "The id has to be a positive integer!\n"
            if sd < 0 or sd > 31 or (sm == 2 and sd > 28) or ((sm == 4 or sm == 6 or sm == 9 or sm == 11) and sd > 30):
                errors += "The day of the rent has to be between 0 and 31!\n"
            if sm < 0 or sm > 12:
                errors += "The month of the rent has to be between 0 and 12!\n"
            if sy < 0 or sy > 4000:
                errors += "The year of the rent has to be between 0 and 4000!\n"
            if rental.get_return_date()!='-':
                end_date=rental.get_return_date().split(".")
                ed = int(end_date[0])
                em = int(end_date[1])
                ey = int(end_date[2])
                if (sd > ed and (sm == em or sm > em) and (sy == ey or sy > ey)) or ((sd == ed or sd > ed) and sm > em and (sy == ey or sy > ey)) or ((sd == ed or sd > ed) and (sm == em or sm > em) and sy > ey):
                    errors += "The dates are wrong!\n"
                if ed < 0 or ed > 31 or (em == 2 and ed > 28) or ((em == 4 or em == 6 or em == 9 or em == 11) and ed > 30):
                    errors += "The day of the return has to be between 0 and 28/30/31(depends on the month)!\n"
                if em < 0 or em > 12:
                    errors += "The month of the return has to be between 0 and 12!\n"
                if ey < 0 or ey > 4000:
                    errors += "The year of the return has to be between 0 and 4000!\n"
        if len(errors) > 0:
            raise ValidError(errors)


class ValidError(Exception):
    pass


class RepoError(Exception):
    pass

class ServError(Exception):
    pass