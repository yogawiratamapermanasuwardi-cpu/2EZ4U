"""
backend/m3_laporan.py
M3: Laporan harian terurut -> insertion sort + binary search

Aturan proyek: tanpa dict, set, sorted, .sort(), heapq, bisect, collections,
literal {} maupun comprehension dict/set. Hanya list sebagai array primitif,
tuple, aritmetika, dan I/O.

Kompleksitas:
    insertion_sort   O(n^2) terburuk/rata-rata, O(n) bila hampir terurut, stabil
    selection_sort   O(n^2) selalu
    bubble_sort      O(n^2) terburuk, O(n) bila sudah terurut (early exit)
    binary_search    O(log n)
    lower/upper_bound O(log n)
    cari_rentang     O(log n) untuk batas + O(k) bila hasil ingin ditampilkan
"""

import csv

# ---------------------------------------------------------------------------
# Skema kolom pesanan.csv
# ---------------------------------------------------------------------------
NAMA_KOLOM = ("oid", "pelanggan", "resto", "menu", "harga",
              "prioritas", "t_masuk_detik", "t_selesai_detik", "status")

K_OID = 0
K_PELANGGAN = 1
K_RESTO = 2
K_MENU = 3
K_HARGA = 4
K_PRIORITAS = 5
K_T_MASUK = 6
K_T_SELESAI = 7
K_STATUS = 8

# kolom bertipe angka (sisanya teks)
_KOLOM_ANGKA = (K_HARGA, K_PRIORITAS, K_T_MASUK, K_T_SELESAI)


def indeks_kolom(nama):
    """Cari indeks kolom dari namanya (pencarian linear pada tuple kecil)."""
    for i in range(len(NAMA_KOLOM)):
        if NAMA_KOLOM[i] == nama:
            return i
    return -1


def detik_ke_jam(detik):
    """86400 detik -> 'HH:MM:SS' (tanpa format dict)."""
    if detik is None:
        return "-"
    j = detik // 3600
    m = (detik % 3600) // 60
    s = detik % 60
    return "%02d:%02d:%02d" % (j, m, s)


# ---------------------------------------------------------------------------
# Pembacaan data
# ---------------------------------------------------------------------------
def baca_pesanan_csv(path, batas=None):
    """
    Baca data/pesanan.csv menjadi list of list (bukan dict).
    Kolom angka dikonversi ke int; t_selesai_detik kosong -> None.
    batas: maksimal jumlah baris yang dibaca (None = semua).
    """
    hasil = []
    with open(path, newline="", encoding="utf-8") as f:
        pembaca = csv.reader(f)          # reader biasa, BUKAN DictReader
        pertama = True
        for baris in pembaca:
            if pertama:                  # lewati header
                pertama = False
                continue
            if len(baris) < 9:
                continue
            rec = [None] * 9
            for k in range(9):
                v = baris[k].strip()
                if k in _KOLOM_ANGKA:
                    rec[k] = int(v) if v != "" else None
                else:
                    rec[k] = v
            hasil.append(rec)
            if batas is not None and len(hasil) >= batas:
                break
    return hasil


# ---------------------------------------------------------------------------
# Statistik algoritma (untuk ditampilkan di UI)
# ---------------------------------------------------------------------------
class StatSort:
    def __init__(self):
        self.banding = 0
        self.geser = 0      # penggeseran / penukaran elemen

    def __str__(self):
        return "%d perbandingan, %d pergeseran" % (self.banding, self.geser)


# ---------------------------------------------------------------------------
# Algoritma sort (in-place, urut menaik, berdasarkan satu kolom)
# ---------------------------------------------------------------------------
def insertion_sort(larik, kolom, stat=None):
    """Insertion sort stabil: sisipkan elemen ke-i ke bagian kiri yang sudah urut."""
    n = len(larik)
    for i in range(1, n):
        item = larik[i]
        kunci = item[kolom]
        j = i - 1
        while j >= 0:
            if stat is not None:
                stat.banding += 1
            if larik[j][kolom] > kunci:
                larik[j + 1] = larik[j]
                if stat is not None:
                    stat.geser += 1
                j -= 1
            else:
                break
        larik[j + 1] = item
    return larik


def selection_sort(larik, kolom, stat=None):
    """Selection sort: pilih minimum dari sisa, tukar ke posisi i. (tidak stabil)"""
    n = len(larik)
    for i in range(n - 1):
        mn = i
        for j in range(i + 1, n):
            if stat is not None:
                stat.banding += 1
            if larik[j][kolom] < larik[mn][kolom]:
                mn = j
        if mn != i:
            tmp = larik[i]
            larik[i] = larik[mn]
            larik[mn] = tmp
            if stat is not None:
                stat.geser += 1
    return larik


def bubble_sort(larik, kolom, stat=None):
    """Bubble sort dengan early exit bila satu putaran tanpa penukaran."""
    n = len(larik)
    for i in range(n - 1):
        tukar = False
        for j in range(n - 1 - i):
            if stat is not None:
                stat.banding += 1
            if larik[j][kolom] > larik[j + 1][kolom]:
                tmp = larik[j]
                larik[j] = larik[j + 1]
                larik[j + 1] = tmp
                tukar = True
                if stat is not None:
                    stat.geser += 1
        if not tukar:
            break
    return larik


# ---------------------------------------------------------------------------
# Binary search (larik HARUS sudah terurut menaik pada kolom yang dicari)
# kolom=None -> larik berisi nilai langsung (mis. list of int)
# ---------------------------------------------------------------------------
def _nilai(larik, i, kolom):
    if kolom is None:
        return larik[i]
    return larik[i][kolom]


def lower_bound(larik, target, kolom=None):
    """Indeks pertama dengan nilai >= target (len(larik) bila tidak ada)."""
    lo = 0
    hi = len(larik)
    while lo < hi:
        mid = (lo + hi) // 2
        if _nilai(larik, mid, kolom) < target:
            lo = mid + 1
        else:
            hi = mid
    return lo


def upper_bound(larik, target, kolom=None):
    """Indeks pertama dengan nilai > target (len(larik) bila tidak ada)."""
    lo = 0
    hi = len(larik)
    while lo < hi:
        mid = (lo + hi) // 2
        if _nilai(larik, mid, kolom) <= target:
            lo = mid + 1
        else:
            hi = mid
    return lo


def binary_search(larik, target, kolom=None, langkah=None):
    """
    Cari satu indeks yang bernilai == target, atau -1 bila tidak ada.
    langkah: list opsional; bila diberikan, tiap iterasi dicatat (lo, mid, hi)
             agar alurnya bisa ditampilkan di antarmuka.
    """
    lo = 0
    hi = len(larik) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if langkah is not None:
            langkah.append((lo, mid, hi))
        v = _nilai(larik, mid, kolom)
        if v == target:
            return mid
        if v < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1


# ---------------------------------------------------------------------------
# Laporan harian
# ---------------------------------------------------------------------------
class Laporan:
    """
    Laporan harian: kumpulan pesanan yang diurutkan berdasarkan satu kolom,
    lalu bisa dicari dengan binary search.

    Contoh:
        lap = Laporan()
        stat = lap.bangun(rows, kolom="t_selesai_detik", algoritma="insertion",
                          hanya_status="DONE", batas=5000)
        lap.cari(40026)
        lap.rentang(28800, 36000)      # pesanan selesai jam 08:00 - 10:00
        print(lap.ringkasan())
    """

    ALGORITMA = ("insertion", "selection", "bubble")

    def __init__(self):
        self._data = []
        self._kolom = -1
        self._nama_kolom = ""
        self._algoritma = ""

    # -- info ---------------------------------------------------------------
    def __len__(self):
        return len(self._data)

    def sudah_dibangun(self):
        return self._kolom >= 0

    def kolom_aktif(self):
        return self._nama_kolom

    # -- membangun ----------------------------------------------------------
    def bangun(self, rows, kolom="t_selesai_detik", algoritma="insertion",
               hanya_status="DONE", batas=None):
        """
        Salin baris yang lolos filter, lalu urutkan.
        - rows          : list of list (urutan kolom = NAMA_KOLOM)
        - kolom         : nama kolom kunci urut
        - algoritma     : 'insertion' | 'selection' | 'bubble'
        - hanya_status  : 'DONE'/'CANCEL'/'ANTRE' atau None untuk semua
        - batas         : maksimal jumlah baris (jaga waktu, sort O(n^2))
        Mengembalikan StatSort.
        """
        k = indeks_kolom(kolom)
        if k < 0:
            raise ValueError("kolom tidak dikenal: " + str(kolom))

        salinan = []
        for r in rows:
            if hanya_status is not None and r[K_STATUS] != hanya_status:
                continue
            if r[k] is None:             # kunci kosong tidak bisa diurutkan
                continue
            salinan.append(r)
            if batas is not None and len(salinan) >= batas:
                break

        stat = StatSort()
        if algoritma == "insertion":
            insertion_sort(salinan, k, stat)
        elif algoritma == "selection":
            selection_sort(salinan, k, stat)
        elif algoritma == "bubble":
            bubble_sort(salinan, k, stat)
        else:
            raise ValueError("algoritma tidak dikenal: " + str(algoritma))

        self._data = salinan
        self._kolom = k
        self._nama_kolom = kolom
        self._algoritma = algoritma
        return stat

    # -- pencarian ----------------------------------------------------------
    def _konversi(self, teks):
        """Ubah input teks dari UI sesuai tipe kolom aktif."""
        if self._kolom in _KOLOM_ANGKA:
            return int(teks)
        return str(teks).strip()

    def cari(self, target, langkah=None):
        """
        Semua pesanan dengan kunci == target.
        Binary search (lower/upper bound) -> O(log n + k).
        """
        self._pastikan()
        t = self._konversi(target)
        awal = lower_bound(self._data, t, self._kolom)
        akhir = upper_bound(self._data, t, self._kolom)
        if langkah is not None:
            binary_search(self._data, t, self._kolom, langkah)
        hasil = []
        for i in range(awal, akhir):
            hasil.append(self._data[i])
        return hasil

    def rentang(self, lo, hi):
        """Semua pesanan dengan lo <= kunci <= hi (inklusif)."""
        self._pastikan()
        a = self._konversi(lo)
        b = self._konversi(hi)
        if a > b:
            tmp = a
            a = b
            b = tmp
        awal = lower_bound(self._data, a, self._kolom)
        akhir = upper_bound(self._data, b, self._kolom)
        hasil = []
        for i in range(awal, akhir):
            hasil.append(self._data[i])
        return hasil

    # -- ringkasan & tampilan ----------------------------------------------
    def ringkasan(self, baris=None):
        """Ringkasan (jumlah, omzet, rata-rata durasi antar) untuk baris/laporan."""
        if baris is None:
            baris = self._data
        n = len(baris)
        omzet = 0
        total_durasi = 0
        n_durasi = 0
        durasi_min = None
        durasi_max = None
        for r in baris:
            omzet += r[K_HARGA]
            if r[K_T_SELESAI] is not None:
                d = r[K_T_SELESAI] - r[K_T_MASUK]
                total_durasi += d
                n_durasi += 1
                if durasi_min is None or d < durasi_min:
                    durasi_min = d
                if durasi_max is None or d > durasi_max:
                    durasi_max = d
        rata = (total_durasi // n_durasi) if n_durasi > 0 else 0
        out = "Jumlah pesanan : %d\n" % n
        out += "Total omzet    : Rp %d\n" % omzet
        if n_durasi > 0:
            out += "Durasi antar   : rata-rata %d dtk, min %d dtk, maks %d dtk\n" % (
                rata, durasi_min, durasi_max)
        return out

    def tampil(self, n=20, baris=None):
        """Teks tabel n baris pertama (dari laporan, atau dari 'baris' bila diberikan)."""
        if baris is None:
            baris = self._data
        total = len(baris)
        tampil_n = n if n < total else total
        out = "%-10s %-22s %-14s %9s %-9s %-9s %s\n" % (
            "oid", "pelanggan", "resto", "harga", "masuk", "selesai", "status")
        out += "-" * 88 + "\n"
        for i in range(tampil_n):
            r = baris[i]
            out += "%-10s %-22s %-14s %9d %-9s %-9s %s\n" % (
                r[K_OID], r[K_PELANGGAN][:22], r[K_RESTO][:14], r[K_HARGA],
                detik_ke_jam(r[K_T_MASUK]), detik_ke_jam(r[K_T_SELESAI]),
                r[K_STATUS])
        if total > tampil_n:
            out += "... (%d baris lainnya)\n" % (total - tampil_n)
        return out

    def _pastikan(self):
        if not self.sudah_dibangun():
            raise RuntimeError("Laporan belum dibangun. Jalankan 'Laporan harian' dulu.")
