import sqlite3

conn = sqlite3.connect('scoring.db')
cursor = conn.cursor()

cursor.execute('''SELECT * FROM detection_results;''')

result = cursor.fetchall()

if result:
    for data in result:
        print("id:", data[0])
        print("label:", data[1])
        print("skor:", data[2])
        print("box:", data[3])
        print("")
print("tidak ada data")

# Commit perubahan dan tutup koneksi
conn.commit()
conn.close()