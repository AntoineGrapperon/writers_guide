import sqlite3
import json
import os

DB_PATH = "snowflake.db"

def init_db():
    """Initialize the database and create the novels table if it doesn't exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS novels (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            data TEXT NOT NULL,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def save_novel(name, data):
    """Save or update a novel in the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    json_data = json.dumps(data)
    cursor.execute("""
        INSERT INTO novels (name, data, updated_at)
        VALUES (?, ?, CURRENT_TIMESTAMP)
        ON CONFLICT(name) DO UPDATE SET
            data = excluded.data,
            updated_at = CURRENT_TIMESTAMP
    """, (name, json_data))
    conn.commit()
    conn.close()

def load_all_novels():
    """Load all novels from the database as a dictionary."""
    if not os.path.exists(DB_PATH):
        init_db()
        return {}
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name, data FROM novels")
    rows = cursor.fetchall()
    conn.close()
    
    return {name: json.loads(data) for name, data in rows}

def delete_novel(name):
    """Delete a novel from the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM novels WHERE name = ?", (name,))
    conn.commit()
    conn.close()
