import sqlite3
conn = sqlite3.connect('database/data.db')
cursor = conn.cursor()

# Add password column if it doesn't exist
cursor.execute('ALTER TABLE users ADD COLUMN password TEXT;')
conn.commit()
conn.close()
