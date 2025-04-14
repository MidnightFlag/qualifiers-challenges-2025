import sqlite3
import os
from config import Config

conn = sqlite3.connect(Config.DATABASE, check_same_thread=False)

def init_db():
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            rootfolder TEXT
        )
    ''')
    conn.commit()

def get_user_by_username(username):
    c = conn.cursor()
    c.execute("SELECT id, username, password, rootfolder FROM users WHERE username=?", (username,))
    user = c.fetchone()
    return user

def get_user_by_id(user_id):
    c = conn.cursor()
    c.execute("SELECT id, username, password, rootfolder FROM users WHERE id=?", (user_id,))
    user = c.fetchone()
    return user

def create_user(username, password, rootfolder):
    c = conn.cursor()
    c.execute("INSERT INTO users (username, password, rootfolder) VALUES (?, ?, ?)",
              (username, password, rootfolder))
    conn.commit()