# Library

An application for a book library. The application stores:
- **Book**: `book_id`, `title`, `author`
- **Client**: `client_id`, `name`
- **Rental**: `rental_id`, `book_id`, `client_id`, `rented_date`, `returned_date`

In this application you can:
1. Manage clients and books. The user can add, remove, update, and list both clients and books.
2. Rent or return a book. A client can rent an available book. A client can return a rented book at any time. Only available books can be rented.
3. Search for clients or books using any one of their fields (e.g. books can be searched for using id, title or author). The search works using partial string matching.
4. Create statistics:
    - Most rented books. This will provide the list of books, sorted in descending order of the number of times they were rented.
    - Most active clients. This will provide the list of clients, sorted in descending order of the number of book rental days they have (e.g. having 2 rented books for 3 days each counts as 2 x 3 = 6 days).
    - Most rented author. This provides the list of books authored, sorted in descending order of the number of rentals their books have.
5. Undo and redo. Each step will undo/redo the previous operation performed by the user.
