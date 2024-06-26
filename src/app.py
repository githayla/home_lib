import uvicorn
from fastapi import FastAPI, HTTPException, Depends
import sqlite3
from pydantic import BaseModel
from typing import List
from home_lib import Library, Book

## Importante: uvicorn app:app --reload

# Tarefas:
# 1 - Instalar o Postman
# 2 - Mudar o armazenamento de arquivo json para sqlite
# 3 - Estudar conceito de CRUD: https://en.wikipedia.org/wiki/Create,_read,_update_and_delete
# 4 - Implementar na API o CRUD
# 5 - Implementar todos os testes (100% coverage)
# 6 - MVC

app = FastAPI()
database = 'Library.db'

# Book Model - This is Pydantic model
class BookBase(BaseModel):
    title: str
    author: str
    publication_year: int
    genre: str
    language: str
    status: str
    serie: int

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int

# This makes the connection with the database
def get_db():
    conn = sqlite3.connect(database)
    try:
        yield conn
    finally: conn.close()


# C - Create
@app.post("/books/", response_model=BookCreate)
def create_book(book: BookCreate, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute(
        '''
        INSERT INTO books (title, author, publication_year, genre, language, status, serie)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''',(book.title, book.author, book.publication_year, book.genre, book.language, book.status, book.serie)
    )
    db.commit()
    book_id = cursor.lastrowid
    return {**book.dict(), "id": book_id}


# R - Read
@app.get("/books/", response_model=List[Book])
def read_books(skip: int = 0, limit: int = 100, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM books LIMIT ? OFFSET ?", (limit, skip))
    rows = cursor.fetchall()
    return [
        {"id": row[0], "title": row[1], "author": row[2], "publication_year": row[3], "genre": row[4], "language": row[5], "status": row[6], "serie": row[7]}
        for row in rows
    ]


# U - Update
# Pesquisar: Patch
@app.put("/books/{book_id}", response_model=Book)
def update_book(book_id: int, book: BookCreate, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute(
        '''
        UPDATE books
        SET title = ?, author = ?, publication_year = ?, genre = ?, language = ?, status = ?, serie = ?
        WHERE id = ?
        ''', (book.title, book.author, book.publication_year, book.genre, book.language, book.status, book.serie, book_id)
    )
    db.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Book not found")
    return {**book.dict(), "id": book_id}


# D - Delete
@app.delete("/books/{book_id}", response_model=Book)
def delete_book(book_id: int, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM books WHERE id = ?", (book_id,))
    row = cursor.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Book not found")
    cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
    db.commit()
    return {"id": row[0], "title": row[1], "author": row[2], "publication_year": row[3], "genre": row[4], "language": row[5], "status": row[6], "serie": row[7]}

if __name__ == '__main__':
   uvicorn.run(app, host ="127.0.0.1", port=8000)