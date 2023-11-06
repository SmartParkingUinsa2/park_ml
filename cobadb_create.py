import sqlite3

# Connect to the database (or create it if it doesn't exist)
conn = sqlite3.connect('cobaparking.db')

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Create the "parking" table
cursor.execute('''CREATE TABLE IF NOT EXISTS parking
                  (filename TEXT, type INTEGER, count INTEGER)''')

# Commit the changes to the database
conn.commit()

# Close the connection
conn.close()