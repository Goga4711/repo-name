import sqlite3
import hashlib

DATABASE = 'users.db'

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    # Добавим пример пользователя
    cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', 
                   ('admin', hashlib.md5('admin'.encode()).hexdigest()))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print('Database initialized!')
