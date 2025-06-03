import cv2  # Import OpenCV untuk pemrosesan citra dan video
import imutils  # Import imutils untuk fungsi utilitas tambahan seperti resize gambar


hog = cv2.HOGDescriptor()  # Membuat objek HOG (Histogram of Oriented Gradients) descriptor
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())  
# Mengatur detector SVM bawaan OpenCV untuk mendeteksi manusia (people detector)

img = cv2.imread("Citra_Hasil.jpg")  
# Membaca gambar dengan nama file 'Pedestrian.jpg' dari folder kerja

img = imutils.resize(img, width=min(400, img.shape[0]))  
# Mengubah ukuran gambar agar lebarnya maksimal 400 piksel 
# dengan mempertahankan rasio aspek; jika tinggi gambar lebih kecil dari 400, gunakan tinggi asli

(regions, _) = hog.detectMultiScale(img, winStride=(4,4), padding=(4,4), scale=1.05)  
# Mendeteksi area yang mungkin berisi manusia pada gambar
# winStride: langkah window sliding
# padding: penambahan piksel di sekitar window untuk deteksi lebih baik
# scale: faktor skala untuk image pyramid, untuk mendeteksi manusia dengan ukuran berbeda

for (x, y, w, h) in regions:  
    # Loop untuk setiap bounding box hasil deteksi (x,y) posisi kiri atas, w=lebar, h=tinggi
    
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)  
    # Menggambar kotak berwarna merah (BGR: (0,0,255)) dengan ketebalan 2 pixel di sekitar manusia yang terdeteksi
    
    cv2.imshow("image", img)  
    # Menampilkan gambar dengan kotak deteksi di jendela bernama 'image'
    
    cv2.waitKey()  
    # Menunggu penekanan tombol agar gambar tetap tampil sampai user menekan tombol
