import sqlite3
import hashlib

def init_db():
    conn = sqlite3.connect('whispervault.db', check_same_thread=False)
    c = conn.cursor()
    
    # Create users table with password
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create messages table
    c.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def get_db_connection():
    conn = sqlite3.connect('whispervault.db', check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    conn = get_db_connection()
    try:
        hashed_password = hash_password(password)
        conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def verify_user(username, password):
    conn = get_db_connection()
    hashed_password = hash_password(password)
    user = conn.execute(
        'SELECT * FROM users WHERE username = ? AND password = ?', 
        (username, hashed_password)
    ).fetchone()
    conn.close()
    return user is not None

def user_exists(username):
    conn = get_db_connection()
    user = conn.execute(
        'SELECT * FROM users WHERE username = ?', 
        (username,)
    ).fetchone()
    conn.close()
    return user is not None

def add_message(username, message):
    conn = get_db_connection()
    try:
        conn.execute('INSERT INTO messages (username, message) VALUES (?, ?)', (username, message))
        conn.commit()
    finally:
        conn.close()

def get_messages():
    conn = get_db_connection()
    try:
        messages = conn.execute('''
            SELECT username, message, created_at 
            FROM messages 
            ORDER BY created_at ASC
        ''').fetchall()
        return messages
    finally:
        conn.close()