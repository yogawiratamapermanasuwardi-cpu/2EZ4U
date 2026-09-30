# frontend/ui.py
import tkinter as tk
from tkinter import ttk

class ProyekUI:
    def __init__(self, root, aksi_handler):
        self.root = root
        self.aksi_handler = aksi_handler
        self.root.title("2EZ4U Food Delivery - M1 Demo")
        self.root.geometry("900x600")

        # --- PANEL KIRI: Daftar Menu ---
        self.frame_kiri = tk.Frame(self.root, width=250, bg="#e0e0e0")
        self.frame_kiri.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)

        tk.Label(self.frame_kiri, text="M1 - DATA PESANAN", bg="#e0e0e0", font=("Arial", 10, "bold")).pack(pady=5)
        
        self.listbox_menu = tk.Listbox(self.frame_kiri, selectmode=tk.SINGLE, height=20, width=35)
        menu_items = [
            "ARRAY - LIHAT PESANAN",
            "ARRAY - TAMBAH PESANAN REGULER",
            "ARRAY - TAMBAH PESANAN PRIORITAS",
            "ARRAY - TAMBAH PESANAN VIP",
            "ARRAY - HAPUS PESANAN",
            "LINKEDLIST - LIHAT PESANAN",
            "LINKEDLIST - TAMBAH PESANAN REGULER",
            "LINKEDLIST - TAMBAH PESANAN PRIORITAS",
            "LINKEDLIST - TAMBAH PESANAN VIP",
            "LINKEDLIST - HAPUS PESANAN"
        ]
        for item in menu_items:
            self.listbox_menu.insert(tk.END, item)
        self.listbox_menu.pack(padx=5, pady=5, fill=tk.Y, expand=True)
        self.listbox_menu.bind("<<ListboxSelect>>", self.on_menu_select)

        # --- PANEL KANAN: Form & Hasil ---
        self.frame_kanan = tk.Frame(self.root)
        self.frame_kanan.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Judul Menu Aktif
        self.lbl_judul = tk.Label(self.frame_kanan, text="Pilih menu di sebelah kiri", font=("Arial", 12, "bold"), anchor="w")
        self.lbl_judul.pack(fill=tk.X, pady=5)

        # Form Parameter (Nama Pesanan / Index)
        self.frame_form = tk.Frame(self.frame_kanan)
        self.frame_form.pack(fill=tk.X, pady=5)
        tk.Label(self.frame_form, text="Parameter (Nama/Index):").pack(side=tk.LEFT)
        self.entry_param = tk.Entry(self.frame_form, width=30)
        self.entry_param.pack(side=tk.LEFT, padx=10)
        self.btn_aksi = tk.Button(self.frame_form, text="EKSEKUSI", bg="#1a3b5c", fg="white", command=self.eksekusi_aksi)
        self.btn_aksi.pack(side=tk.LEFT)

        # Layar Hasil Utama
        tk.Label(self.frame_kanan, text="Isi Struktur Data:", anchor="w").pack(fill=tk.X, pady=(10, 0))
        self.text_hasil = tk.Text(self.frame_kanan, height=15, state=tk.DISABLED)
        self.text_hasil.pack(fill=tk.BOTH, expand=True, pady=5)

        # --- PANEL BAWAH: Command Log ---
        tk.Label(self.frame_kanan, text="COMMAND LOG (Waktu Eksekusi):", anchor="w").pack(fill=tk.X)
        self.text_log = tk.Text(self.frame_kanan, height=6, bg="black", fg="lime", state=tk.DISABLED)
        self.text_log.pack(fill=tk.X, pady=5)

        self.menu_aktif = None

    def on_menu_select(self, event):
        selection = self.listbox_menu.curselection()
        if selection:
            self.menu_aktif = self.listbox_menu.get(selection[0])
            self.lbl_judul.config(text=self.menu_aktif)

    def eksekusi_aksi(self):
        if not self.menu_aktif:
            return
        param = self.entry_param.get()
        # Memanggil fungsi controller/handler di app.py
        self.aksi_handler(self.menu_aktif, param)
        self.entry_param.delete(0, tk.END)

    def update_hasil(self, teks):
        self.text_hasil.config(state=tk.NORMAL)
        self.text_hasil.delete(1.0, tk.END)
        self.text_hasil.insert(tk.END, teks)
        self.text_hasil.config(state=tk.DISABLED)

    def tambah_log(self, teks):
        self.text_log.config(state=tk.NORMAL)
        self.text_log.insert(tk.END, teks + "\n")
        self.text_log.see(tk.END)
        self.text_log.config(state=tk.DISABLED)