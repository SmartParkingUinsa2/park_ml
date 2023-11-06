import sqlite3

# Connect to the database
conn = sqlite3.connect('cobaparking.db')

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Define the data dictionary
data = [
    {'filename': 'coba.jpg', 'type': 1, 'count': 4}
]

# Insert data into the "parking" table
for item in data:
    cursor.execute("INSERT INTO parking (filename, type, count) VALUES (?, ?, ?)",
                   (item['filename'], item['type'], item['count']))

# Commit the changes to the database
conn.commit()

# Close the connection
conn.close()

# Add success
print("Data added successfully")

# Close the connection
conn.close()