from flask import Flask, request
import sqlite3

app = Flask(__name__)

@app.route('/store', methods=['POST'])
def store_data():
    # Get the data from the request
    data = request.get_json()

    # Connect to the database
    conn = sqlite3.connect('parking.db')
    cursor = conn.cursor()

    # Insert data into the "parking" table
    filename = data['filename']
    tipe = data['tipe']
    count = data['count']
    cursor.execute("INSERT INTO parking (filename, type, count) VALUES (?, ?, ?)", (filename, tipe, count))

    # Commit the changes to the database
    conn.commit()

    # Close the connection
    conn.close()

    return 'Data stored in the database.'

if __name__ == '__main__':
    app.run(port=5001)