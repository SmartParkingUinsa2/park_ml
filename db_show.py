import sqlite3

# Connect to the database
conn = sqlite3.connect('db_ml.db')

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Retrieve data from the "parking" table
cursor.execute("SELECT * FROM deteksi")
data = cursor.fetchall()
conn.commit()

# Print the data
for row in data:
    print(row)

# Close the connection
conn.close()