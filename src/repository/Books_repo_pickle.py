from domain.entities import Book
from validation.validators import RepoError
import pickle
import os


class BooksBinary(object):
    def __init__(self, file_name):  # file_name='Books.pickle'
        self.file_name = file_name
        self.books = []
        self.read_from_binary_file()

    def read_from_binary_file(self):
        if os.path.getsize(self.file_name) > 0:
            with open(self.file_name, "rb") as file:
                try:
                    while 1:
                        repo = pickle.load(file)
                        self.books.append(repo)
                except EOFError:
                    return []
                except IOError as ioe:
                    raise IOError(ioe)
            return repo

    def write_in_binary_file(self, books):
        # ["id", "title", "author"]
        with open(self.file_name, "wb") as file:
            for book in books:
                pickle.dump(book, file)
        file.close()

    def add(self, book):
        books = self.books
        if book in self.books:
            raise RepoError("This book already exists!")
        book_id = book.get_book_id()
        title = book.get_title()
        author = book.get_author()
        books.append(Book(int(book_id), title, author))
        self.write_in_binary_file(books)

    def remove(self, book):
        if book not in self.books:
            raise RepoError("This book doesn't exist!")
        index = self.books.index(book)
        self.books.pop(index)
        self.write_in_binary_file(self.books)

    def update(self, book, new_title, new_author):
        if book not in self.books:
            raise RepoError("This book doesn't exist!")
        book.set_title(new_title)
        book.set_author(new_author)
        self.write_in_binary_file(self.books)

    def get_all(self):
        return self.books[:]

    def get_book_by_id(self, book_id):
        for current_book in self.books:
            if int(current_book.get_book_id()) == int(book_id):
                return current_book
        raise RepoError("This book doesn't exist!")

    def get_book_by_partial_id(self, book_id):
        book_by_id_list = []
        for current_book in self.books:
            current_book_id = str(current_book.get_book_id())
            book_id = str(book_id)
            if book_id in current_book_id:
                book_by_id_list.append(current_book)
        if len(book_by_id_list) == 0:
            raise RepoError("There is no book with this id!")
        return book_by_id_list

    def get_book_by_partial_title(self, book_title):
        book_by_title_list = []
        for current_book in self.books:
            current_book_title = current_book.get_title()
            current_book_title = current_book_title.casefold()
            book_title = book_title.casefold()
            if book_title in current_book_title:
                book_by_title_list.append(current_book)
        if len(book_by_title_list) == 0:
            raise RepoError("There is no book with this title!")
        return book_by_title_list

    def get_book_by_partial_author(self, book_author):
        book_by_author_list = []
        for current_book in self.books:
            current_book_author = current_book.get_author()
            current_book_author = current_book_author.casefold()
            book_author = book_author.casefold()
            if book_author in current_book_author:
                book_by_author_list.append(current_book)
        if len(book_by_author_list) == 0:
            raise RepoError("There is no book with this author!")
        return book_by_author_list

    def get_book_title_by_id(self, book_id):
        for current_book in self.books:
            if int(current_book.get_book_id()) == int(book_id):
                title = current_book.get_title()
                return title
        raise RepoError("This book doesn't exist!")

    def get_book_author_by_id(self, book_id):
        for current_book in self.books:
            if int(current_book.get_book_id()) == int(book_id):
                author = current_book.get_author()
                return author
        raise RepoError("This book doesn't exist!")
