from unittest import TestCase
from domain.entities import Book, Client
from validation.validators import RepoError


class Tests(TestCase):
    def __init__(self, servBook, servClient, repoBook, repoClient, validBook, validClient):
        self.__test_book_list = []
        self.__test_client_list = []
        self.__servBook = servBook
        self.__servClient = servClient
        self.__repoBook = repoBook
        self.__repoClient = repoClient
        self.__validBook = validBook
        self.__validClient = validClient

    def run_all_tests(self):
        self.test_add_b_repo()
        self.test_remove_b_repo()
        self.test_update_b_repo()
        self.test_add_c_repo()
        self.test_remove_c_repo()
        self.test_update_c_repo()
        self.test_add_book()
        self.test_remove_book()
        self.test_update_book()
        self.test_add_client()
        self.test_remove_client()
        self.test_update_client()

    def test_add_b_repo(self):
        book_id = "28"
        title = "Sing, Unburied, Sing"
        author = "Jesmyn Ward"
        book = Book(book_id, title, author)
        book_id_test = int(book.get_book_id())
        book_title_test = book.get_title()
        book_author_test = book.get_author()
        self.__validBook.validate_book(book)
        self.assertTrue(book not in self.__test_book_list)
        self.__test_book_list.append(book)
        self.assertTrue(book_id_test == 28)
        self.assertTrue(book_title_test == "Sing, Unburied, Sing")
        self.assertTrue(book_author_test == "Jesmyn Ward")

    def test_remove_b_repo(self):
        book_id = "28"
        title = "Sing, Unburied, Sing"
        author = "Jesmyn Ward"
        book = Book(book_id, title, author)
        self.assertTrue(book in self.__test_book_list)
        index = self.__test_book_list.index(book)
        self.__test_book_list.pop(index)
        assert book not in self.__test_book_list

    def test_update_b_repo(self):
        book_id = "72"
        title = "Artemis"
        author = "Andy Weir"
        book = Book(book_id, title, author)
        self.__validBook.validate_book(book)
        self.__repoBook.add(book)
        book = self.__repoBook.get_book_by_id(book_id)
        new_title = "Heather, The Totality"
        new_author = "Matthew Weiner"
        self.__repoBook.update(book, new_title, new_author)
        self.__validBook.validate_book(book)
        check_title = book.get_title()
        check_author = book.get_author()
        self.__test_book_list.append(book)
        assert check_author == "Matthew Weiner" and check_title == "Heather, The Totality"
        index = self.__test_book_list.index(book)
        self.__test_book_list.pop(index)
        self.__repoBook.remove(book)

    def test_add_c_repo(self):
        client_id = "25"
        name = "Sorescu Dan"
        client = Client(client_id, name)
        self.__test_client_list.append(client)
        assert client in self.__test_client_list

    def test_remove_c_repo(self):
        client_id = "75"
        name = "Cantemir Valentina"
        client = Client(client_id, name)
        self.__validClient.validate_client(client)
        self.__test_client_list.append(client)
        self.assertTrue(client in self.__test_client_list)
        index = self.__test_client_list.index(client)
        self.__test_client_list.pop(index)
        assert client not in self.__test_client_list

    def test_update_c_repo(self):
        client_id = "58"
        name = "Patron Corina"
        client = Client(client_id, name)
        self.__validClient.validate_client(client)
        self.__repoClient.add(client)
        client = self.__repoClient.get_client_by_id(client_id)
        new_name = "Dumitriu Marian"
        self.__repoClient.update(client, new_name)
        self.__validClient.validate_client(client)
        check_name = client.get_name()
        assert check_name == "Dumitriu Marian"
        client = self.__repoClient.get_client_by_id(client_id)
        self.__repoClient.remove(client)

    def test_add_book(self):
        book_id = "22"
        title = "By the Numbers"
        author = "James Richardson"
        book = Book(book_id, title, author)
        self.__validBook.validate_book(book)
        self.__repoBook.add(book)
        check_title = book.get_title()
        check_author = book.get_author()
        assert check_author == "James Richardson" and check_title == "By the Numbers"

    def test_remove_book(self):
        book_id = "22"
        book = self.__repoBook.get_book_by_id(book_id)
        self.__repoBook.remove(book)
        assert book not in self.__test_book_list

    def test_update_book(self):
        book_id = "29"
        title = "Wait"
        author = "C.K. Williams"
        new_title = "The Man with the Baltic Stare"
        new_author = "James Church"
        book = Book(book_id, title, author)
        self.__validBook.validate_book(book)
        self.__repoBook.add(book)
        book = self.__repoBook.get_book_by_id(book_id)
        self.__repoBook.update(book, new_title, new_author)
        self.__validBook.validate_book(book)
        check_title = book.get_title()
        check_author = book.get_author()
        assert check_author == "James Church" and check_title == "The Man with the Baltic Stare"
        self.__repoBook.remove(book)

    def test_add_client(self):
        client_id = "7"
        name = "Diaconu Doriana"
        client = Client(client_id, name)
        self.__validClient.validate_client(client)
        self.__repoClient.add(client)
        check_name = client.get_name()
        assert check_name == "Diaconu Doriana"

    def test_remove_client(self):
        client_id = "7"
        client = self.__repoClient.get_client_by_id(client_id)
        self.__repoClient.remove(client)
        assert client not in self.__test_client_list

    def test_update_client(self):
        client_id = "71"
        name = "Benegui Lorena"
        new_name = "Iordache Gabriel"
        client = Client(client_id, name)
        self.__validClient.validate_client(client)
        self.__repoClient.add(client)
        client = self.__repoClient.get_client_by_id(client_id)
        self.__repoClient.update(client, new_name)
        self.__validClient.validate_client(client)
        check_name = client.get_name()
        assert check_name == "Iordache Gabriel"
        self.__repoClient.remove(client)
