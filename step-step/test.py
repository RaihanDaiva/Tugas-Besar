import cv2

hog = cv2.HOGDescriptor()  # Inisialisasi HOG Descriptor
img = cv2.imread("Citra_Asli.jpg")  # Membaca gambar
fitur = hog.compute(img)  # Menghitung fitur HOG dari gambar
print(fitur.shape)  # Menampilkan bentuk dari fitur HOG yang dihasilkan
print(fitur)  # Menampilkan nilai fitur HOG