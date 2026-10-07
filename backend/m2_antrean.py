"""
backend/m2_antrean.py
M2: AntreanMelingkar (circular queue) + Tumpukan (stack) untuk fitur Undo.

Aturan proyek: tanpa dict, set, sorted, .sort(), heapq, bisect, collections,
literal {} maupun comprehension dict/set. List dipakai hanya sebagai
array primitif (alokasi [None] * kapasitas, akses lewat indeks).
"""


class AntreanMelingkar:
    """
    Antrean FIFO berbasis array melingkar.

    - depan  : indeks elemen paling depan
    - ukuran : jumlah elemen yang tersimpan
    - indeks belakang = (depan + ukuran) % kapasitas

    Kompleksitas:
        enqueue      O(1) amortized (O(n) saat kapasitas dilipat dua)
        dequeue      O(1)
        push_depan   O(1) amortized  (dipakai untuk undo "layani")
        pop_belakang O(1)            (dipakai untuk undo "enqueue")
        peek         O(1)
    """

    def __init__(self, kapasitas=8):
        if kapasitas < 1:
            kapasitas = 1
        self._data = [None] * kapasitas
        self._kap = kapasitas
        self._depan = 0
        self._ukuran = 0
        self._jumlah_resize = 0

    # ---------- util internal ----------
    def _lipat_dua(self):
        kap_baru = self._kap * 2
        baru = [None] * kap_baru
        i = 0
        while i < self._ukuran:
            baru[i] = self._data[(self._depan + i) % self._kap]
            i += 1
        self._data = baru
        self._kap = kap_baru
        self._depan = 0
        self._jumlah_resize += 1

    # ---------- operasi utama ----------
    def enqueue(self, x):
        if self._ukuran == self._kap:
            self._lipat_dua()
        idx = (self._depan + self._ukuran) % self._kap
        self._data[idx] = x
        self._ukuran += 1

    def dequeue(self):
        if self._ukuran == 0:
            return None
        x = self._data[self._depan]
        self._data[self._depan] = None
        self._depan = (self._depan + 1) % self._kap
        self._ukuran -= 1
        return x

    def push_depan(self, x):
        """Sisipkan di depan antrean (untuk membatalkan dequeue)."""
        if self._ukuran == self._kap:
            self._lipat_dua()
        self._depan = (self._depan - 1 + self._kap) % self._kap
        self._data[self._depan] = x
        self._ukuran += 1

    def pop_belakang(self):
        """Cabut elemen paling belakang (untuk membatalkan enqueue)."""
        if self._ukuran == 0:
            return None
        idx = (self._depan + self._ukuran - 1) % self._kap
        x = self._data[idx]
        self._data[idx] = None
        self._ukuran -= 1
        return x

    def peek(self):
        if self._ukuran == 0:
            return None
        return self._data[self._depan]

    def kosong(self):
        return self._ukuran == 0

    def __len__(self):
        return self._ukuran

    def get(self, i):
        """Elemen ke-i dari depan (0-based), O(1)."""
        if i < 0 or i >= self._ukuran:
            return None
        return self._data[(self._depan + i) % self._kap]

    def ke_list(self, batas=None):
        """Salinan isi antrean urut dari depan (batas = maks elemen)."""
        n = self._ukuran
        if batas is not None and batas < n:
            n = batas
        hasil = [None] * n
        i = 0
        while i < n:
            hasil[i] = self._data[(self._depan + i) % self._kap]
            i += 1
        return hasil

    def stats(self):
        return ("AntreanMelingkar ukuran=" + str(self._ukuran)
                + " kapasitas=" + str(self._kap)
                + " depan=" + str(self._depan)
                + " resize=" + str(self._jumlah_resize))


class Tumpukan:
    """
    Stack LIFO berbasis array dinamis (kapasitas dilipat dua saat penuh).

    Kompleksitas: push O(1) amortized, pop O(1), peek O(1).
    """

    def __init__(self, kapasitas=8):
        if kapasitas < 1:
            kapasitas = 1
        self._data = [None] * kapasitas
        self._kap = kapasitas
        self._top = 0  # jumlah elemen = indeks slot kosong berikutnya

    def push(self, x):
        if self._top == self._kap:
            kap_baru = self._kap * 2
            baru = [None] * kap_baru
            i = 0
            while i < self._top:
                baru[i] = self._data[i]
                i += 1
            self._data = baru
            self._kap = kap_baru
        self._data[self._top] = x
        self._top += 1

    def pop(self):
        if self._top == 0:
            return None
        self._top -= 1
        x = self._data[self._top]
        self._data[self._top] = None
        return x

    def peek(self):
        if self._top == 0:
            return None
        return self._data[self._top - 1]

    def kosong(self):
        return self._top == 0

    def __len__(self):
        return self._top

    def stats(self):
        return ("Tumpukan ukuran=" + str(self._top)
                + " kapasitas=" + str(self._kap))


# Jenis aksi yang bisa di-undo (disimpan di Tumpukan sebagai tuple)
AKSI_MASUK = "MASUK"      # pesanan baru masuk antrean  -> undo: cabut dari belakang
AKSI_LAYANI = "LAYANI"    # pesanan dilayani (dequeue)  -> undo: kembalikan ke depan


class LayananAntrean:
    """
    Fasad untuk UI M2:
        - isi_antrean()       -> "Isi antrean FIFO"
        - layani_berikutnya() -> "Layani berikutnya"
        - undo()              -> "Undo"
    """

    def __init__(self, kapasitas=8):
        self.antrean = AntreanMelingkar(kapasitas)
        self.riwayat = Tumpukan()

    def muat_dari_pesanan(self, baris_pesanan, status_antre="ANTRE"):
        """
        baris_pesanan: list of list/tuple hasil baca CSV
        (urutan kolom: oid, pelanggan, resto, menu, harga, prioritas,
         t_masuk_detik, t_selesai_detik, status).
        Hanya pesanan berstatus ANTRE yang dimasukkan. Tidak dicatat ke
        riwayat undo karena ini pemuatan awal.
        """
        i = 0
        n = len(baris_pesanan)
        while i < n:
            b = baris_pesanan[i]
            if b[8] == status_antre:
                self.antrean.enqueue(b)
            i += 1
        return len(self.antrean)

    def tambah(self, pesanan):
        self.antrean.enqueue(pesanan)
        self.riwayat.push((AKSI_MASUK, pesanan))

    def layani_berikutnya(self):
        p = self.antrean.dequeue()
        if p is None:
            return None
        self.riwayat.push((AKSI_LAYANI, p))
        return p

    def undo(self):
        """Batalkan aksi terakhir. Return (jenis_aksi, pesanan) atau None."""
        aksi = self.riwayat.pop()
        if aksi is None:
            return None
        jenis = aksi[0]
        pesanan = aksi[1]
        if jenis == AKSI_MASUK:
            self.antrean.pop_belakang()
        elif jenis == AKSI_LAYANI:
            self.antrean.push_depan(pesanan)
        return aksi

    def isi_antrean(self, batas=50):
        return self.antrean.ke_list(batas)

    def stats(self):
        return self.antrean.stats() + " | " + self.riwayat.stats()


if __name__ == "__main__":
    # uji cepat
    s = LayananAntrean(kapasitas=2)
    s.tambah("O-1")
    s.tambah("O-2")
    s.tambah("O-3")          # memicu resize
    print(s.isi_antrean())   # ['O-1', 'O-2', 'O-3']
    print(s.layani_berikutnya())  # O-1
    print(s.isi_antrean())   # ['O-2', 'O-3']
    print(s.undo())          # ('LAYANI', 'O-1')
    print(s.isi_antrean())   # ['O-1', 'O-2', 'O-3']
    print(s.undo())          # ('MASUK', 'O-3')
    print(s.isi_antrean())   # ['O-1', 'O-2']
    print(s.stats())
