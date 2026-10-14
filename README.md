# Proyek 2EZ4U APP
**Studi Kasus Proyek Akhir**  
**Mata Kuliah:** Struktur Data & Analisa Algoritma (EC234303)  
**Departemen Teknik Komputer, FTEIC - Institut Teknologi Sepuluh Nopember**  

---

## 1. Deskripsi Proyek
**2EZ4U APP** adalah mini *backend engine* dan antarmuka desktop untuk sistem layanan antar makanan/barang (mirip GoFood/GrabFood/ShopeeFood). Proyek ini dirancang untuk menangani beban dataset berskala 200.000 data pesanan (`pesanan.csv`) dengan menerapkan struktur data primitif dan algoritma buatan sendiri dari nol tanpa menggunakan *instant function* bawaan Python (seperti `dict`, `set`, `sorted`, `sort()`, `collections`, `heapq`, `bisect`, atau literal `{}`).

---

## 2. Struktur Repositori
```text
2EZ4U/
├── README.md        <- Laporan dokumentasi & analisa
├── app.py           <- Berkas utama untuk menjalankan aplikasi ("python app.py")
├── data/
│   ├── pesanan.csv  <- Dataset 200.000 data pesanan
│   └── peta.csv     <- Data graf peta lokasi rute
├── backend/
│   ├── __init__.py
│   ├── m1_pesanan.py <- M1: Array Dinamis & Singly Linked List
│   ├── m2_antrean.py <- M2: Stack (Kasir, Undo/Redo) & Queue (Naif vs Melingkar)
│   ├── m3_laporan.py <- M3: Insertion Sort, Merge Sort, Linear Search, Binary Search
│   └── m3_sorting.py <- Alias modul sorting
└── frontend/
    ├── __init__.py
    └── ui.py         <- Antarmuka Tkinter (3 bagian: Menu, Form/Hasil, COMMAND)
