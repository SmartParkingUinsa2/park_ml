import sqlite3

# Connect to the database
conn = sqlite3.connect('cobaparking.db')

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Retrieve data from the "parking" table
cursor.execute("SELECT * FROM parking")
data = cursor.fetchall()

# Print the data
print(f"filename \t type \t count")
for row in data:
    filename, type, count = row
    print(f"{filename} \t {type} \t {count}")

# Close the connection
conn.close()