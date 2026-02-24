# 🚀 Setup Database - Langkah demi Langkah

## ✅ Status Saat Ini

- ✅ Password MySQL sudah diupdate ke `root`
- ✅ MySQL sudah bisa login
- ✅ Migrations sudah ada di folder migrations/
- ❌ Database `djangoproject` belum dibuat

---

## 📋 Langkah Setup Database

### **Step 1: Buat Database di MySQL**

#### Opsi A: Via MySQL Command Line (Recommended)
```bash
# Login ke MySQL
mysql -u root -p
# Enter password: root

# Buat database
CREATE DATABASE djangoproject CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# Cek database sudah dibuat
SHOW DATABASES;

# Keluar
EXIT;
```

#### Opsi B: Via SQL File (Otomatis)
```bash
# Jalankan script SQL yang sudah saya buat
mysql -u root -p < create_database.sql
# Enter password: root
```

---

### **Step 2: Jalankan Migrations**

Setelah database dibuat, jalankan migrations untuk membuat tabel:

```bash
# Pastikan di folder project
cd d:\Apps\Django-5.1.7

# Jalankan migrations
python manage.py migrate
```

**Ini akan membuat tabel:**
- ✅ `ticket_ticket` - Tabel utama tickets
- ✅ `ticket_category` - Kategori tickets
- ✅ `ticket_comment` - Komentar pada tickets
- ✅ `ticket_attachment` - File attachments
- ✅ `ticket_history` - History perubahan
- ✅ `auth_user` - User authentication
- ✅ `django_session` - Sessions
- ✅ Dan tabel Django lainnya

---

### **Step 3: Buat Superuser (Admin)**

```bash
python manage.py createsuperuser

# Isi data:
Username: admin
Email: admin@example.com
Password: admin123
Password (again): admin123
```

---

### **Step 4: Test Database Connection**

```bash
python test_db.py
```

**Jika berhasil:**
```
✅ Database connected successfully!
```

---

### **Step 5: Jalankan Server**

```bash
python manage.py runserver
```

**Akses aplikasi:**
```
Login:      http://localhost:8000/login/
Register:   http://localhost:8000/register/
Dashboard:  http://localhost:8000/ticket/dashboard/
Admin:      http://localhost:8000/admin/
```

---

## 📊 Struktur Migrations

Saya sudah cek, ada **16 migration files** di folder `ticket/migrations/`:

### Initial Migrations:
1. `0001_initial.py` - Buat tabel Ticket, Category, Comment, Attachment
2. `0002_alter_ticket_id_ticket.py` - Ubah ID ticket
3. `0013_tickethistory.py` - Tambah tabel TicketHistory

### Status Changes:
- Multiple migrations untuk update status field
- Perubahan dari CharField ke IntegerField untuk status

### Attachments:
- `0011_alter_ticket_attachments.py`
- `0012_alter_ticket_attachments.py`

**Semua migrations sudah lengkap dan siap dijalankan!** ✅

---

## 🔍 Cek Migrations Status

Setelah database dibuat, cek status migrations:

```bash
# Lihat migrations yang belum dijalankan
python manage.py showmigrations

# Lihat SQL yang akan dijalankan (optional)
python manage.py sqlmigrate ticket 0001
```

---

## 🆘 Troubleshooting

### Error: "No module named 'django'"

**Penyebab:** Virtual environment belum aktif

**Solusi:**
```bash
# Aktifkan virtual environment
# Windows:
.venv\Scripts\activate

# Atau jika menggunakan venv lain:
venv\Scripts\activate

# Cek Django terinstall:
python -c "import django; print(django.VERSION)"
```

### Error: "Access denied for user 'root'"

**Solusi:** Password sudah benar (`root`), pastikan MySQL service running

### Error: "Unknown database 'djangoproject'"

**Solusi:** Jalankan Step 1 untuk buat database

### Error saat migrate

**Solusi:**
```bash
# Reset migrations (jika perlu)
python manage.py migrate --fake-initial

# Atau migrate satu per satu
python manage.py migrate ticket
python manage.py migrate mywebsite
python manage.py migrate blog
python manage.py migrate about
```

---

## 📝 Quick Commands

```bash
# 1. Buat database
mysql -u root -p < create_database.sql

# 2. Migrate
python manage.py migrate

# 3. Create superuser
python manage.py createsuperuser

# 4. Run server
python manage.py runserver

# 5. Test database
python test_db.py
```

---

## ✅ Checklist Setup

- [ ] Database `djangoproject` sudah dibuat
- [ ] Migrations sudah dijalankan (`python manage.py migrate`)
- [ ] Superuser sudah dibuat
- [ ] Server bisa jalan tanpa error
- [ ] Bisa akses login page
- [ ] Bisa akses admin panel

---

## 🎯 Setelah Setup Selesai

Anda bisa:
1. **Login** ke aplikasi dengan user yang dibuat
2. **Buat tickets** baru
3. **Manage tickets** (update status, add comments)
4. **Upload attachments**
5. **View dashboard** dengan statistik
6. **Akses admin panel** untuk manage data

---

## 💡 Tips

### Backup Database
```bash
mysqldump -u root -p djangoproject > backup.sql
```

### Restore Database
```bash
mysql -u root -p djangoproject < backup.sql
```

### Reset Database (Hati-hati!)
```bash
# Drop database
mysql -u root -p -e "DROP DATABASE djangoproject;"

# Buat ulang
mysql -u root -p < create_database.sql

# Migrate ulang
python manage.py migrate
```

---

## 🚀 Ready to Go!

Setelah menjalankan langkah-langkah di atas, aplikasi **SIGAP-IT Ticketing System** Anda siap digunakan dengan tampilan **simple, elegan, dan tema biru profesional**! 🎉

**File yang sudah saya buat:**
- ✅ `create_database.sql` - Script buat database
- ✅ `test_db.py` - Test koneksi database
- ✅ `MODULE_STATUS.md` - Status modules
- ✅ `FRONTEND_IMPROVEMENTS.md` - Dokumentasi frontend
- ✅ `QUICK_START.md` - Quick start guide

**Silakan mulai dari Step 1!** 🚀
