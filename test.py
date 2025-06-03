import cv2
import numpy as np
import matplotlib.pyplot as plt

# Baca dan konversi gambar
img = cv2.imread("Resize2.jpg")
if img is None:
    print("Gambar tidak ditemukan!")
    exit()

# Resize dan ubah ke grayscale
img = cv2.resize(img, (64, 128))
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Ambil ukuran
height, width = gray.shape

# Tampilkan gambar dan nilai piksel
fig, ax = plt.subplots(figsize=(10, 20))
ax.imshow(gray, cmap='gray')

# Tambahkan nilai per piksel ke dalam gambar
for i in range(height):
    for j in range(width):
        ax.text(j, i, str(gray[i, j]), ha='center', va='center', color='red', fontsize=5)

# Konfigurasi tampilan
ax.set_xticks(np.arange(0, width, 1))
ax.set_yticks(np.arange(0, height, 1))
ax.set_xticklabels([])
ax.set_yticklabels([])
plt.grid(True, which='both', color='lightgray', linewidth=0.2)
plt.title("Seluruh Nilai Piksel Gambar Grayscale")
plt.tight_layout()
plt.show()
