import tkinter as tk
import time
import os
from frontend.ui import ProyekUI
from backend.m1_pesanan import Array, LinkList

class MainApp:
    def __init__(self):
        self.root = tk.Tk()
        # Inisialisasi struktur data M1
        self.arr = Array()
        self.ll = LinkList()
        
        # Inisialisasi UI dan pasang fungsi handler
        self.ui = ProyekUI(self.root, self.proses_aksi)

    def muat_data_csv(self):
        mulai = time.perf_counter()
        jumlah_dimuat = 0
        path_csv = os.path.join("data", "pesanan.csv")
        
        try:
            # Membaca file secara manual tanpa library tambahan
            with open(path_csv, 'r', encoding='utf-8') as f:
                header = True
                for baris in f:
                    if header:
                        header = False # Lewati baris pertama (judul kolom)
                        continue
                    
                    kolom = baris.strip().split(',')
                    if len(kolom) >= 2:
                        oid = kolom[0]
                        pelanggan = kolom[1]
                        data_pesanan = f"{oid} - {pelanggan}"
                        
                        # Masukkan ke dalam struktur data Array dan Linked List
                        self.arr.append(data_pesanan)
                        self.ll.append(data_pesanan)
                        jumlah_dimuat += 1
                        
            selesai = time.perf_counter()
            waktu_ms = (selesai - mulai) * 1000
            pesan = f"Sukses memuat {jumlah_dimuat} baris dari pesanan.csv!\nWaktu: {waktu_ms:.2f} ms"
            self.ui.update_hasil(pesan)
            self.ui.tambah_log(f"> LOAD DATA CSV | Waktu: {waktu_ms:.2f} ms")
            
        except FileNotFoundError:
            self.ui.update_hasil(f"Error: File '{path_csv}' tidak ditemukan! Pastikan ada folder 'data' yang berisi 'pesanan.csv'.")

    def proses_aksi(self, menu, param):
        # 1. Definisikan variabel di awal untuk mencegah UnboundLocalError
        mulai = time.perf_counter()
        hasil_teks = ""

        # --- LOGIKA LOAD DATA ---
        if menu == "DATA - LOAD":
            self.muat_data_csv()
            return # Hentikan eksekusi di sini karena fungsi muat_data sudah mencatat log sendiri

        # --- LOGIKA ARRAY ---
        if "ARRAY" in menu:
            if "LIHAT PESANAN" in menu:
                hasil_teks = "Menampilkan data Array saat ini."
            elif "TAMBAH PESANAN REGULER" in menu:
                self.arr.append(param)
                hasil_teks = f"Reguler '{param}' ditambahkan di belakang Array."
            elif "TAMBAH PESANAN PRIORITAS" in menu:
                tengah = self.arr.size // 2
                self.arr.insert(tengah, param)
                hasil_teks = f"Prioritas '{param}' ditambahkan di tengah Array (index {tengah})."
            elif "TAMBAH PESANAN VIP" in menu:
                self.arr.insert(0, param)
                hasil_teks = f"VIP '{param}' ditambahkan di depan Array (index 0)."
            elif "HAPUS PESANAN" in menu:
                try:
                    idx = int(param)
                    if 0 <= idx < self.arr.size:
                        self.arr.delete(idx)
                        hasil_teks = f"Pesanan pada index {idx} dihapus dari Array."
                    else:
                        hasil_teks = f"Error: Index {idx} di luar batas Array."
                except ValueError:
                    hasil_teks = "Error: Parameter hapus harus berupa angka index."
            
            # Tampilkan isi Array saat ini (Dibatasi 100 agar UI tidak hang jika data banyak)
            limit = min(self.arr.size, 100)
            isi_sekarang = [self.arr.get(i) for i in range(limit)]
            tampilan = f"{hasil_teks}\n\nIsi Array (Total: {self.arr.size} | Menampilkan {limit} teratas):\n{isi_sekarang}"
            if self.arr.size > limit:
                tampilan += "\n... (data selanjutnya disembunyikan agar aplikasi tidak lag)"
            self.ui.update_hasil(tampilan)

        # --- LOGIKA LINKED LIST ---
        elif "LINKEDLIST" in menu:
            if "LIHAT PESANAN" in menu:
                hasil_teks = "Menampilkan data Linked List saat ini."
            elif "TAMBAH PESANAN REGULER" in menu:
                self.ll.append(param)
                hasil_teks = f"Reguler '{param}' ditambahkan di belakang Linked List."
            elif "TAMBAH PESANAN PRIORITAS" in menu:
                tengah = self.ll.size // 2
                self.ll.insert(tengah, param)
                hasil_teks = f"Prioritas '{param}' ditambahkan di tengah Linked List (posisi {tengah})."
            elif "TAMBAH PESANAN VIP" in menu:
                self.ll.insert(0, param)
                hasil_teks = f"VIP '{param}' ditambahkan di depan Linked List."
            elif "HAPUS PESANAN" in menu:
                try:
                    idx = int(param)
                    if 0 <= idx < self.ll.size:
                        self.ll.delete(idx)
                        hasil_teks = f"Pesanan pada posisi {idx} dihapus dari Linked List."
                    else:
                        hasil_teks = f"Error: Index {idx} di luar batas Linked List."
                except ValueError:
                    hasil_teks = "Error: Parameter hapus harus berupa angka posisi."
            
            # Tampilkan isi Linked List saat ini (Dibatasi 100 agar UI tidak hang)
            limit = min(self.ll.size, 100)
            isi_sekarang = [self.ll.get(i) for i in range(limit)]
            tampilan = f"{hasil_teks}\n\nIsi Linked List (Total: {self.ll.size} | Menampilkan {limit} teratas):\n{isi_sekarang}"
            if self.ll.size > limit:
                tampilan += "\n... (data selanjutnya disembunyikan agar aplikasi tidak lag)"
            self.ui.update_hasil(tampilan)

        # Catat waktu eksekusi ke kotak hitam di bawah
        selesai = time.perf_counter()
        waktu_ms = (selesai - mulai) * 1000
        log_msg = f"> {menu} | Param: '{param}' | Waktu: {waktu_ms:.5f} ms"
        self.ui.tambah_log(log_msg)

    def jalankan(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = MainApp()
    app.jalankan()