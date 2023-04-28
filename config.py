import os
import sqlite3

SQLALCHEMY_DATABASE_URI = 'sqlite:///C:/Users/79257/PycharmProjects/pythonTESTDOC/doc.db'
db_path = SQLALCHEMY_DATABASE_URI[len('sqlite:'):]

if not os.path.exists(db_path):
    connection = sqlite3.connect('doc.db')
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS document (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            content TEXT NOT NULL,
            is_deleted TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS document_version (
            id INTEGER PRIMARY KEY,
            document_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS document_deletion (
            id INTEGER PRIMARY KEY,
            document_id INTEGER UNIQUE NOT NULL,
            deleted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    connection.commit()
    connection.close()
