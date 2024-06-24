import sqlite3
import json


def read_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data


def insert_data(db_path, table, data):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    for book in data:
        columns = ', '.join(book.keys())
        placeholders = ', '.join(['?'] * len(book))
        sql = f'INSERT INTO {table} ({columns}) VALUES ({placeholders})'
        cursor.execute(sql, tuple(book.values()))

    conn.commit()
    conn.close()


def main():
    jsonFile = 'library.json'
    db_path = 'Library.db'
    table = 'books'

    # Read data from JSON file
    data = read_file(jsonFile)

    # Insert data into SQLite database
    insert_data(db_path, table, data)


if __name__ == '__main__':
    main()
