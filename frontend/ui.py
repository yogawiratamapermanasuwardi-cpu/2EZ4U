# frontend/ui.py
import tkinter as tk

# ---------------------------------------------------------------------------
# Daftar menu (teks menu dipakai app.py untuk percabangan, jangan diubah
# kalau handler M1/M2/Tumpukan di app.py sudah memakai teks ini)
# ---------------------------------------------------------------------------
M1_ITEMS = [
    "ARRAY - LIHAT PESANAN",
    "ARRAY - TAMBAH PESANAN REGULER",
    "ARRAY - TAMBAH PESANAN PRIORITAS",
    "ARRAY - TAMBAH PESANAN VIP",
    "ARRAY - HAPUS PESANAN",
    "LINKEDLIST - LIHAT PESANAN",
    "LINKEDLIST - TAMBAH PESANAN REGULER",
    "LINKEDLIST - TAMBAH PESANAN PRIORITAS",
    "LINKEDLIST - TAMBAH PESANAN VIP",
    "LINKEDLIST - HAPUS PESANAN",
]

M2_ITEMS = [
    "ANTREAN - ENQUEUE (tambah pesanan)",
    "ANTREAN - DEQUEUE (proses pesanan)",
    "ANTREAN - PUSH DEPAN (untuk pesanan VIP/prioritas)",
    "ANTREAN - POP BELAKANG",
    "ANTREAN - PEEK",
    "ANTREAN - LIHAT ANTREAN",
]

# Tumpukan (stack/undo) termasuk M2 menurut README proyek
TUMPUKAN_ITEMS = [
    "TUMPUKAN - PUSH (tambah pesanan)",
    "TUMPUKAN - POP (hapus pesanan)",
    "TUMPUKAN - PEEK (lihat pesanan teratas)",
    "TUMPUKAN - LIHAT TUMPUKAN",
]

# M3 = laporan terurut (insertion sort + binary search)
M3_ITEMS = [
    "LAPORAN - BANGUN LAPORAN HARIAN",
    "LAPORAN - CARI DI LAPORAN",
    "LAPORAN - CARI RENTANG",
]

# (menu, petunjuk parameter) -> dicari linear, tanpa dict
HINT_MENU = (
    ("LAPORAN - BANGUN LAPORAN HARIAN",
     "Format: kolom,algoritma,batas  (contoh: t_selesai_detik,insertion,5000). "
     "Kosong = default. algoritma: insertion / selection / bubble"),
    ("LAPORAN - CARI DI LAPORAN",
     "Isi nilai kunci yang dicari sesuai kolom laporan (contoh: 40026)"),
    ("LAPORAN - CARI RENTANG",
     "Format: batas_bawah,batas_atas  (contoh: 28800,36000)"),
)


class ProyekUI:
    def __init__(self, root, aksi_handler):
        self.root = root
        self.aksi_handler = aksi_handler
        self.root.title("2EZ4U Food Delivery")
        self.root.geometry("1100x780")

        # --- PANEL KIRI: Daftar Menu ---
        self.frame_kiri = tk.Frame(self.root, width=280, bg="#e0e0e0")
        self.frame_kiri.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)

        self.listbox_menu_m1 = self._buat_menu("M1 - DATA PESANAN", M1_ITEMS, 10)
        self.listbox_menu = self.listbox_menu_m1   # alias nama lama
        self.listbox_menu_m2 = self._buat_menu("M2 - ANTREAN PESANAN", M2_ITEMS, 6)
        self.listbox_menu_tumpukan = self._buat_menu("M2 - TUMPUKAN (UNDO)", TUMPUKAN_ITEMS, 4)
        self.listbox_menu_m3 = self._buat_menu("M3 - LAPORAN HARIAN", M3_ITEMS, 3)

        self._semua_listbox = [
            self.listbox_menu_m1,
            self.listbox_menu_m2,
            self.listbox_menu_tumpukan,
            self.listbox_menu_m3,
        ]

        # --- PANEL KANAN: Form & Hasil ---
        self.frame_kanan = tk.Frame(self.root)
        self.frame_kanan.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.lbl_judul = tk.Label(self.frame_kanan, text="Pilih menu di sebelah kiri",
                                  font=("Arial", 12, "bold"), anchor="w")
        self.lbl_judul.pack(fill=tk.X, pady=5)

        self.frame_form = tk.Frame(self.frame_kanan)
        self.frame_form.pack(fill=tk.X, pady=5)
        tk.Label(self.frame_form, text="Parameter (Nama/Index):").pack(side=tk.LEFT)
        self.entry_param = tk.Entry(self.frame_form, width=40)
        self.entry_param.pack(side=tk.LEFT, padx=10)
        self.btn_aksi = tk.Button(self.frame_form, text="EKSEKUSI", bg="#1a3b5c",
                                  fg="white", command=self.eksekusi_aksi)
        self.btn_aksi.pack(side=tk.LEFT)

        # Petunjuk parameter untuk menu terpilih
        self.lbl_hint = tk.Label(self.frame_kanan, text="", anchor="w", justify=tk.LEFT,
                                 fg="#555555", wraplength=700)
        self.lbl_hint.pack(fill=tk.X)

        # Layar hasil utama
        tk.Label(self.frame_kanan, text="Isi Struktur Data:", anchor="w").pack(fill=tk.X, pady=(10, 0))
        self.text_hasil = tk.Text(self.frame_kanan, height=15, state=tk.DISABLED,
                                  font=("Courier New", 9))
        self.text_hasil.pack(fill=tk.BOTH, expand=True, pady=5)

        # --- PANEL BAWAH: Command Log ---
        tk.Label(self.frame_kanan, text="COMMAND LOG (Waktu Eksekusi):", anchor="w").pack(fill=tk.X)
        self.text_log = tk.Text(self.frame_kanan, height=6, bg="black", fg="lime",
                                state=tk.DISABLED)
        self.text_log.pack(fill=tk.X, pady=5)

        self.menu_aktif = None

    # ------------------------------------------------------------------
    # Pembuat listbox menu (satu fungsi untuk semua modul)
    # ------------------------------------------------------------------
    def _buat_menu(self, judul, items, tinggi):
        tk.Label(self.frame_kiri, text=judul, bg="#e0e0e0",
                 font=("Arial", 10, "bold")).pack(pady=(8, 2))
        lb = tk.Listbox(self.frame_kiri, selectmode=tk.SINGLE, height=tinggi,
                        width=42, exportselection=False)
        for item in items:
            lb.insert(tk.END, item)
        lb.pack(padx=5, pady=2)
        lb.bind("<<ListboxSelect>>", lambda e, kotak=lb: self._pilih_menu(kotak))
        return lb

    def _pilih_menu(self, kotak):
        pilihan = kotak.curselection()
        if not pilihan:
            return
        # hanya satu menu yang boleh terpilih di seluruh panel kiri
        for lb in self._semua_listbox:
            if lb is not kotak:
                lb.selection_clear(0, tk.END)
        self.menu_aktif = kotak.get(pilihan[0])
        self.lbl_judul.config(text=self.menu_aktif)
        self.lbl_hint.config(text=self._hint_untuk(self.menu_aktif))

    def _hint_untuk(self, menu):
        for i in range(len(HINT_MENU)):
            if HINT_MENU[i][0] == menu:
                return HINT_MENU[i][1]
        return ""

    # Nama lama tetap disediakan agar kode lain yang memanggilnya tidak error
    def on_menu_select(self, event):
        self._pilih_menu(self.listbox_menu_m1)

    def on_menu_select_m2(self, event):
        self._pilih_menu(self.listbox_menu_m2)

    def on_menu_select_m3(self, event):
        self._pilih_menu(self.listbox_menu_m3)

    # ------------------------------------------------------------------
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