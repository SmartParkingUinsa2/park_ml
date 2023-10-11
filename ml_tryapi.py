import requests

url = 'https://xpqht97q-5000.asse.devtunnels.ms/upload'
file_path = 'img\coba4.jpg'

with open(file_path, 'rb') as file:
    response = requests.post(url, files={'file': file})

print(response.text)