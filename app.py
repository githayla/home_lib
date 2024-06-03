from flask import Flask, request, render_template, redirect, url_for
from home_lib import Library, Book

app = Flask(__name__)
library = Library()

@app.route('/')
def home():
    return render_template('home.html', books=library.get_books())

@app.route('/add', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        publication_year = request.form['publication_year']
        genre = request.form['genre']
        language = request.form['language']
        status = request.form['status']
        serie = request.form['serie']
        new_book = Book(title, author, publication_year, genre, language, status, serie)
        library.add_book(new_book)
        return redirect(url_for('home'))
    return render_template('add_book.html')

@app.route('/search', methods=['GET', 'POST'])
def search_books():
    if request.method == 'POST':
        author = request.form['author']
        found_books = library.search_by_author(author)
        return render_template('search_results.html', books=found_books, author=author)
    return render_template('search_books.html')

if __name__ == '__main__':
    app.run(debug=True)
