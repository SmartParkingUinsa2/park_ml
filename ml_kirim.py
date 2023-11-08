import requests

# server URL
url = 'https://xpqht97q-5000.asse.devtunnels.ms/upload'

# file path
file_path = 'img\coba5.jpg'

# send file to server
with open(file_path, 'rb') as file:
    response = requests.post(url, files={'file': file})

print(response.text)