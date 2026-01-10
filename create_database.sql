-- Script untuk membuat database Django
-- Jalankan di MySQL dengan: mysql -u root -p < create_database.sql

-- Buat database jika belum ada
CREATE DATABASE IF NOT EXISTS djangoproject CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Gunakan database
USE djangoproject;

-- Tampilkan database yang sudah dibuat
SHOW DATABASES;

-- Tampilkan info
SELECT 'Database djangoproject berhasil dibuat!' AS Status;
