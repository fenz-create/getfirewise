import sqlite3

conn = sqlite3.connect("firewise.db")
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password TEXT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS schools (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    school_name TEXT NOT NULL,
    contact_person TEXT,
    email TEXT,
    status TEXT DEFAULT 'Not Signed Up',
    scheduled_date TEXT,
    completion_date TEXT,
    firefighter_visit_date TEXT
)
""")

conn.commit()
conn.close()
