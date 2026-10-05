import sqlite3

conn = sqlite3.connect("hashlab.db")
conn.execute("ALTER TABLE tests ADD COLUMN entered_by TEXT")
conn.commit()
conn.close()
