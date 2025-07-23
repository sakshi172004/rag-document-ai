# app/db.py
import sqlite3
import os

DB_PATH = os.path.join("data", "metadata.db")
DATA_DIR = "data"

def init_db():
    # Make sure the data directory exists
    os.makedirs(DATA_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Simple table to just keep track of filenames
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY,
            filename TEXT NOT NULL UNIQUE,
            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def add_document(filename: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Using 'OR IGNORE' is a simple way to avoid errors on duplicates
    cursor.execute("INSERT OR IGNORE INTO documents (filename) VALUES (?)", (filename,))
    conn.commit()
    conn.close()

def get_all_documents():
    conn = sqlite3.connect(DB_PATH)
    # This makes the output a dictionary, which is nice.
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT id, filename, uploaded_at FROM documents ORDER BY id DESC")
    docs = cursor.fetchall()
    conn.close()
    # Convert Row objects to plain dicts for FastAPI
    return [dict(row) for row in docs]