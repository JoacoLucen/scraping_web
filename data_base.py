import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).parent / "noticias.db"

def save_titles(news_media, titles):
    """Save news titles to the SQLite database.
    Args:
        medio (str): The news source.
        titles (list): A list of news titles."""
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS titles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        news_media TEXT,
        title TEXT,
        date TEXT
    )
    """)
    
    date = datetime.now().strftime("%Y-%m-%d")
    for t in titles:
        cursor.execute(
            "INSERT INTO titles (news_media, title, date) VALUES (?, ?, ?)", (news_media, t, date)
        )
    
    conn.commit()
    conn.close()
