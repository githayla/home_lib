import json
import os

class Book:
    def __init__(self, title, author, publication_year, genre, language, status, serie):
        self.title = title
        self.author = author
        self.publication_year = publication_year
        self.genre = genre
        self.language = language
        self.status = status
        self.serie = serie
    
    #The following function converts a 'book' object into a dic (JSON compatible format) -> necessary to save the data of the book to a json file
    def to_dict(self):
        return {
            'title': self.title,
            'author': self.author,
            'publication_year': self.publication_year,
            'genre': self.genre,
            'language': self.language,
            'status': self.status,
            'serie': self.serie
        }

class Library:
    def __init__(self, filepath='library.json'):
        self.filepath = filepath
        self.books = self.load_books()
    
    def load_books(self):
        if os.path.exists(self.filepath):
            with open(self.filepath, 'r') as file:
                return [Book(**data) for data in json.load(file)]
        return []
    
    def save_books(self):
        with open(self.filepath, 'w') as file:
            json.dump([book.to_dict() for book in self.books], file, indent=7)

#check if the book is already added before adding it to the json
    def book_exists(self, title, author):
        for book in self.books:
            if book.title == title and book.author == author:
                return True
        return False
    
    def add_book(self,book):
        if not self.book_exists(book.title, book.author):
            self.books.append(book)
            self.save_books()

    def get_books(self):
        return self.books 
    
    def search_by_author(self, author):
        found_books = []
        for book in self.books:
            if book.author.lower() == author.lower():
                found_books.append(book)
        return found_books    