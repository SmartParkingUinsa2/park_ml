from flask import Flask, request
import requests
import os

app = Flask(__name__)

# assign upload folder
UPLOAD_FOLDER = 'img2'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename)) # put file into folder

    data = {'filename': file.filename,
            'tipe': 1,
            'count': 50}

    # send data to db server
    url = 'https://xpqht97q-5001.asse.devtunnels.ms/store'
    requests.post(url, json=data)

    return "data_saved"

# run flask app
if __name__ == '__main__':
    app.run(port=5000)