* 2EZ4U APP - Engine Backend Layanan Antar Makanan

Proyek ini adalah implementasi engine backend untuk layanan antar makanan dan barang skala mini, dikembangkan untuk Proyek Akhir mata kuliah Struktur Data & Analisa Algoritma (EC234303) Departemen Teknik Komputer, FTEIC-ITS[cite: 1]. 

** Struktur Aplikasi
Aplikasi ini dibangun dengan tiga lapisan utama[cite: 1]:
1. **Data**: Simulasi database menggunakan file CSV yang terdiri dari 200.000 baris data pesanan dan data peta[cite: 1].
2. **Backend**: Implementasi struktur data dan algoritma dari nol, tanpa menggunakan fungsi instan bawaan Python seperti `dict` atau `list.sort()`[cite: 1, 2].
3. **Frontend**: Antarmuka pengguna grafis berbasis Tkinter untuk memvisualisasikan alur proses dan mengukur waktu eksekusi operasi[cite: 1, 2].

** Progres Pengembangan
Pengembangan dilakukan secara bertahap. Saat ini, fitur yang telah diselesaikan mencakup hingga Milestone 2 (M2)[cite: 2]:

*   M1: Larik (Array) vs Rantai (Linked List)**[cite: 2]
    *   Menyimpan data pesanan ke dalam struktur Array dan Linked List secara paralel untuk membandingkan performa keduanya[cite: 6].
    *   Mendukung operasi lihat, tambah, dan hapus pesanan[cite: 2].
    *   Implementasi aturan bisnis penyisipan pesanan: Reguler (diurutkan di belakang), Prioritas (menyisip ke tengah), dan VIP (langsung di urutan pertama)[cite: 6].
*   M2: Antrean dan Tumpukan**[cite: 2]
    *   Implementasi struktur data Queue (Antrean) untuk manajemen pemrosesan pesanan[cite: 2, 3].
    *   Implementasi struktur data Stack (Tumpukan) untuk menjalankan fitur pembatalan operasi atau Undo[cite: 2, 3].

** Prasyarat dan Cara Menjalankan
   **Kebutuhan Sistem**: Python 3.11 atau versi lebih baru[cite: 1].

**Langkah Eksekusi:**
1. Clone repositori ini ke dalam sistem lokal Anda.
2. Pastikan file `pesanan.csv` dan `peta.csv` sudah ditempatkan dengan benar di dalam direktori `data/`[cite: 3].
3. Jalankan aplikasi melalui terminal dengan mengeksekusi file utama:
   `python frontend/app.py`[cite: 3]
