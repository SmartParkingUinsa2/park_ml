import requests
import json

def kirim_foto_ke_url(url, nama_file, pesan):
    try:
        with open(nama_file, 'rb') as file:
            files = {'file': (nama_file, file)}
            data = {'pesan': pesan}
            response = requests.post(url, files=files, data=data)
            if response.status_code == 200:
                print("Foto berhasil terkirim!")

                # Menerima pesan dari server sebagai respons JSON
                pesan_dari_server = response.json()
                if pesan_dari_server:
                    print("Pesan dari server:", pesan_dari_server)
                else:
                    print("Server tidak mengirim pesan.")

            else:
                print("Gagal mengirim foto. Kode status:", response.status_code)
    except Exception as e:
        print("Terjadi kesalahan:", str(e))

# Ganti 'nama_file' dengan nama file foto yang ingin Anda kirim
nama_file = 'gambar\coba5.jpg'

# Ganti 'url_tujuan' dengan URL tempat Anda ingin mengirim foto
url_tujuan = 'http://sj7ks71n-5000.asse.devtunnels.ms/deteksi'

# Pesan yang ingin Anda kirim
pesan = {
    'info': 'Ini adalah pesan dari klien.'
}

kirim_foto_ke_url(url_tujuan, nama_file, pesan)
