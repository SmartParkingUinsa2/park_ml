CREATE DATABASE IF NOT EXISTS db_ml;
USE db_ml;

-- Table 'gambar'
CREATE TABLE IF NOT EXISTS gambar (
    id_gambar INTEGER PRIMARY KEY AUTOINCREMENT,
    path_gambar VARCHAR(255),
    size_gambar INTEGER
);

-- Table deteksi
CREATE TABLE IF NOT EXISTS deteksi (
    id_deteksi INTEGER PRIMARY KEY AUTOINCREMENT,
    id_gambar INTEGER,
    tahun INTEGER,
    bulan INTEGER,
    tanggal INTEGER,
    hari VARCHAR(6),
    jam INTEGER,
    area VARCHAR(5),
    jenis_kendaraan VARCHAR(12),
    jumlah_kendaraan INTEGER
);
