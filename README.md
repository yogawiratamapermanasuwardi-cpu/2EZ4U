* 2EZ4U APP - Engine Backend Layanan Antar Makanan

Proyek ini adalah implementasi engine backend untuk layanan antar makanan dan barang skala mini, dikembangkan untuk Proyek Akhir mata kuliah Struktur Data & Analisa Algoritma (EC234303) Departemen Teknik Komputer, FTEIC-ITS. 

** Struktur Aplikasi
Aplikasi ini dibangun dengan tiga lapisan utama:
1. **Data**: Simulasi database menggunakan file CSV yang terdiri dari 200.000 baris data pesanan dan data peta.
2. **Backend**: Implementasi struktur data dan algoritma dari nol, tanpa menggunakan fungsi instan bawaan Python seperti `dict` atau `list.sort()`.
3. **Frontend**: Antarmuka pengguna grafis berbasis Tkinter untuk memvisualisasikan alur proses dan mengukur waktu eksekusi operasi.

** Progres Pengembangan
Pengembangan dilakukan secara bertahap. Saat ini, fitur yang telah diselesaikan mencakup hingga Milestone 2 (M2):

*   M1: Larik (Array) vs Rantai (Linked List)**
    *   Menyimpan data pesanan ke dalam struktur Array dan Linked List secara paralel untuk membandingkan performa keduanya.
    *   Mendukung operasi lihat, tambah, dan hapus pesanan.
    *   Implementasi aturan bisnis penyisipan pesanan: Reguler (diurutkan di belakang), Prioritas (menyisip ke tengah), dan VIP (langsung di urutan pertama).
      
*   M2: Antrean dan Tumpukan**
    *   Implementasi struktur data Queue (Antrean) untuk manajemen pemrosesan pesanan.
    *   Implementasi struktur data Stack (Tumpukan) untuk menjalankan fitur pembatalan operasi atau Undo.
      
*   M3: Laporan Terurut (Sorting)**[cite: 2]
    *   Penerapan berbagai macam algoritma pengurutan (sorting) seperti *insertion sort*[cite: 2, 3].
    *   Menyajikan laporan data pesanan yang sudah terurut[cite: 2].

** Prasyarat dan Cara Menjalankan
   **Kebutuhan Sistem**: Python 3.11 atau versi lebih baru.

**Langkah Eksekusi:**
1. Clone repositori ini ke dalam sistem lokal Anda.
2. Pastikan file `pesanan.csv` dan `peta.csv` sudah ditempatkan dengan benar di dalam direktori `data/`.
3. Jalankan aplikasi melalui terminal dengan mengeksekusi file utama:
   `python frontend/app.py`
