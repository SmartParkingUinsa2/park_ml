import sqlite3

conn = sqlite3.connect('scoring.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS detection_results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    class_label TEXT,
                    score REAL,
                    bounding_box TEXT
                );''')

# Commit perubahan dan tutup koneksi
conn.commit()
conn.close()