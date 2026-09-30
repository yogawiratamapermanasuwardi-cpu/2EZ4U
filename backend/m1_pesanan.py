# backend/m1_pesanan.py

class Array:
    def __init__(self):
        # Array berukuran tetap awal
        self.capacity = 4
        self.size = 0
        self.data = [None] * self.capacity 

    def _resize(self):
        # Sesuai aturan: alokasi petak baru 2x lipat, salin isi lama
        new_capacity = self.capacity * 2
        new_data = [None] * new_capacity
        for i in range(self.size):
            new_data[i] = self.data[i]
        self.data = new_data
        self.capacity = new_capacity

    def append(self, v):
        # Tambah REGULER (paling belakang) - amortized O(1)
        if self.size == self.capacity:
            self._resize()
        self.data[self.size] = v
        self.size += 1

    def insert(self, i, v):
        # Tambah VIP (i=0) & PRIORITAS (i=tengah) - O(n) karena menggeser elemen
        if self.size == self.capacity:
            self._resize()
        for j in range(self.size, i, -1):
            self.data[j] = self.data[j - 1]
        self.data[i] = v
        self.size += 1

    def get(self, i):
        # Lihat pesanan ke-i - O(1)
        if 0 <= i < self.size:
            return self.data[i]
        return None

    def delete(self, i):
        # Hapus pesanan ke-i - O(n) karena menggeser sisa elemen
        if 0 <= i < self.size:
            for j in range(i, self.size - 1):
                self.data[j] = self.data[j + 1]
            self.data[self.size - 1] = None
            self.size -= 1


class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

class LinkList:
    def __init__(self):
        self.head = None
        # Penunjuk tail wajib disimpan agar tambah di belakang tetap O(1)
        self.tail = None 
        self.size = 0

    def append(self, v):
        # Tambah REGULER (paling belakang) - O(1)
        new_node = Node(v)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self.size += 1

    def insert(self, i, v):
        # Tambah VIP (i=0) -> O(1), PRIORITAS (i=tengah) -> O(n) telusur
        new_node = Node(v)
        if i == 0:
            new_node.next = self.head
            self.head = new_node
            if self.size == 0:
                self.tail = new_node
        else:
            current = self.head
            for _ in range(i - 1):
                if current.next is not None:
                    current = current.next
            new_node.next = current.next
            current.next = new_node
            if new_node.next is None:
                self.tail = new_node
        self.size += 1

    def get(self, i):
        # Lihat pesanan ke-i - O(n)
        current = self.head
        for _ in range(i):
            if current is not None:
                current = current.next
        return current.value if current else None
        
    def delete(self, i):
        # Hapus pesanan ke-i - O(n) telusur
        if self.head is None:
            return
        if i == 0:
            self.head = self.head.next
            if self.head is None:
                self.tail = None
        else:
            current = self.head
            for _ in range(i - 1):
                if current.next is not None:
                    current = current.next
            if current.next is not None:
                if current.next == self.tail:
                    self.tail = current
                current.next = current.next.next
        self.size -= 1