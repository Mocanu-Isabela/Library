from domain.entities import Book
from validation.validators import RepoError


class BooksFile(object):
    def __init__(self, file_name):  # file_name='Books.txt'
        self.file_name = file_name

    def read_from_text_file(self):
        with open(self.file_name, "rt") as file:
            books=[]
            lines = file.readlines()
            for line in lines:
                if len(line) > 1:
                    line = line[:len(line)-1].split(';')
                    books.append(Book(int(line[0]), line[1], line[2]))
        file.close()
        return books

    def append_in_text_file(self, book):
        with open(self.file_name, "at") as file:
            file.write(str(book.get_book_id()) + ";" + book.get_title() + ";" + book.get_author() + '\n')
        file.close()

    def write_in_text_file(self, books):
        with open(self.file_name, "wt") as file:
            for book in books:
                file.write(str(book.get_book_id()) + ";" + book.get_title() + ";" + book.get_author() + '\n')
        file.close()

    def add(self, book):
        books = self.read_from_text_file()
        if book in books:
            raise RepoError("This book already exists!")
        self.append_in_text_file(book)

    def remove(self, book):
        books = self.read_from_text_file()
        if book not in books:
            raise RepoError("This book doesn't exist!")
        index = books.index(book)
        books.pop(index)
        self.write_in_text_file(books)

    def update(self, book, new_title, new_author):
        books = self.read_from_text_file()
        if book not in books:
            raise RepoError("This book doesn't exist!")
        book.set_title(new_title)
        book.set_author(new_author)
        self.write_in_text_file(books)

    def get_all(self):
        books = self.read_from_text_file()
        return books[:]

    def get_book_by_id(self, book_id):
        books = self.read_from_text_file()
        for current_book in books:
            if int(current_book.get_book_id()) == int(book_id):
                return current_book
        raise RepoError("This book doesn't exist!")

    def get_book_by_partial_id(self, book_id):
        books = self.read_from_text_file()
        book_by_id_list = []
        for current_book in books:
            current_book_id = str(current_book.get_book_id())
            book_id = str(book_id)
            if book_id in current_book_id:
                book_by_id_list.append(current_book)
        if len(book_by_id_list) == 0:
            raise RepoError("There is no book with this id!")
        return book_by_id_list

    def get_book_by_partial_title(self, book_title):
        books = self.read_from_text_file()
        book_by_title_list = []
        for current_book in books:
            current_book_title = current_book.get_title()
            current_book_title = current_book_title.casefold()
            book_title = book_title.casefold()
            if book_title in current_book_title:
                book_by_title_list.append(current_book)
        if len(book_by_title_list) == 0:
            raise RepoError("There is no book with this title!")
        return book_by_title_list

    def get_book_by_partial_author(self, book_author):
        books = self.read_from_text_file()
        book_by_author_list = []
        for current_book in books:
            current_book_author = current_book.get_author()
            current_book_author = current_book_author.casefold()
            book_author = book_author.casefold()
            if book_author in current_book_author:
                book_by_author_list.append(current_book)
        if len(book_by_author_list) == 0:
            raise RepoError("There is no book with this author!")
        return book_by_author_list

    def get_book_title_by_id(self, book_id):
        books = self.read_from_text_file()
        for current_book in books:
            if int(current_book.get_book_id()) == int(book_id):
                title = current_book.get_title()
                return title
        raise RepoError("This book doesn't exist!")

    def get_book_author_by_id(self, book_id):
        books = self.read_from_text_file()
        for current_book in books:
            if int(current_book.get_book_id()) == int(book_id):
                author = current_book.get_author()
                return author
        raise RepoError("This book doesn't exist!")
