import sqlite3
from flask import g, current_app

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(current_app.config['DATABASE'])
        db.row_factory = sqlite3.Row
    return db

def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    # Убрали with current_app.app_context() так как он уже есть в app.py
    db = get_db()
    cursor = db.cursor()
    
    # Таблица пользователей
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    
    # Таблица клиентов
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    ''')
    
    # Таблица задач
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            client_id INTEGER,
            user_id INTEGER,
            description TEXT,
            status TEXT,
            deadline TEXT,
            planned_time TEXT,
            FOREIGN KEY(client_id) REFERENCES clients(id),
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')
    
    # Таблица ботов
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            bot_name TEXT NOT NULL,
            bot_token TEXT NOT NULL,
            is_active INTEGER DEFAULT 1,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id))
    ''')
    
    # Добавляем несколько тестовых клиентов
    cursor.execute("INSERT OR IGNORE INTO clients (name) VALUES ('Клиент 1')")
    cursor.execute("INSERT OR IGNORE INTO clients (name) VALUES ('Клиент 2')")
    cursor.execute("INSERT OR IGNORE INTO clients (name) VALUES ('Клиент 3')")
    
    db.commit()