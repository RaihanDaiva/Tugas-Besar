import sys
import cv2
import numpy as np
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from matplotlib import pyplot as plt
import pandas as pd
import imutils  # Import imutils for additional utility functions like image resizing


class ShowImage(QMainWindow):
    def __init__(self):
        super(ShowImage, self).__init__()
        loadUi('GUI.ui', self)
        self.Image = None
        self.button_LoadCitraAsli.clicked.connect(self.load)
        self.button_SaveCitraAsli.clicked.connect(self.saveAsli)
        self.button_SaveCitraHasil.clicked.connect(self.saveHasil)
        self.action_Grayscale.triggered.connect(self.grayscale)
        self.action_Biner.triggered.connect(self.biner)
        # self.button_Brightness.clicked.connect(self.brightness)
        # self.button_Contrast.clicked.connect(self.contrast)
        self.button_Sharpening.clicked.connect(self.sharpening)
        self.button_simulateDay.clicked.connect(self.simulate_day)
        self.button_Smoothing.clicked.connect(self.smoothing)
        self.button_ResetFilter.clicked.connect(self.imgReset)
        self.actionEqualization.triggered.connect(self.equalization)

        self.button_SaveCitraTxt.clicked.connect(self.saveTxt)
        self.button_SaveCitraXlsx.clicked.connect(self.saveExcel)

        self.slider_brightness.setMinimum(-100)
        self.slider_brightness.setMaximum(100)
        self.slider_brightness.setValue(0)  # Default = no brightness change
        self.slider_brightness.valueChanged.connect(self.update_image)

        self.slider_contrast.setMinimum(-100)
        self.slider_contrast.setMaximum(100)
        self.slider_contrast.setValue(0)  # Default = no brightness change
        self.slider_contrast.valueChanged.connect(self.update_image)

        self.button_deteksiManusia.clicked.connect(self.DeteksiManusia)

        self.Image_ori = None
        self.Image_reset = None

    # Fungsi untuk membaca citra
    def load(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Pilih Gambar", "", "Image Files (*.png *.jpg *.jpeg *.bmp)")

        if file_name:
            self.Image = cv2.imread(file_name)
            self.Image_ori = self.Image
            self.Image_reset = self.Image
            if self.Image is None:
                QMessageBox.warning(self, "Error", "Gagal membaca gambar.")
                return
            self.displayImage(1)

    # Fungsi untuk menyimpan citra hasil
    def saveHasil(self):
        if self.Image is None:
            QMessageBox.warning(self, "Error", "Belum ada citra yang dimuat atau diolah.")
            return

        success = cv2.imwrite('Citra_Hasil.jpg', self.Image)
        if success:
            QMessageBox.information(self, "Berhasil", "Citra berhasil disimpan sebagai 'Citra_Hasil.jpg'.")
        else:
            QMessageBox.warning(self, "Gagal", "Gagal menyimpan citra.")

    # Fungsi untuk menyimpan citra asli
    def saveAsli(self):
        if self.Image is None:
            QMessageBox.warning(self, "Error", "Belum ada citra yang dimuat.")
            return

        success = cv2.imwrite('Citra_Asli.jpg', self.Image)
        if success:
            QMessageBox.information(self, "Berhasil", "Citra berhasil disimpan sebagai 'Citra_Asli.jpg'.")
        else:
            QMessageBox.warning(self, "Gagal", "Gagal menyimpan citra.")

    def saveTxt(self):
        if self.Image is None:
            print("No image to save.")
            return

        np.savetxt("Citra_Hasil.txt",
                   self.Image.reshape(-1, self.Image.shape[-1]) if self.Image.ndim == 3 else self.Image, fmt='%d')
        QMessageBox.information(self, "Berhasil", "Citra berhasil disimpan sebagai 'Citra_Hasil.txt'.")
        print(f"Image saved as text to 'Citra_Hasil.txt'")

    def saveExcel(self):
        if self.Image is None:
            print("No image to save.")
            return

            # If RGB image
        if self.Image.ndim == 3:
            # Save each channel in separate sheets
            with pd.ExcelWriter("Citra_Hasil.xlsx") as writer:
                for i, channel in enumerate(['Blue', 'Green', 'Red']):  # OpenCV uses BGR order
                    df = pd.DataFrame(self.Image[:, :, i])
                    df.to_excel(writer, sheet_name=channel, index=False, header=False)
        else:
            # Grayscale
            df = pd.DataFrame(self.Image)
            df.to_excel("Citra_Hasil.xlsx", index=False, header=False)

        QMessageBox.information(self, "Berhasil", "Citra berhasil disimpan sebagai 'Citra_Hasil.xlsx'.")

    # Fungsi untuk mengubah menjadi grayscale
    def grayscale(self):
        # Cek apakah gambar sudah dimuat
        if self.Image is None:
            QMessageBox.warning(self, "Error", "Belum ada citra yang dimuat.")
            return

        # Periksa apakah gambar berwarna
        if len(self.Image.shape) == 3 and self.Image.shape[2] == 3:
            # Konversi ke float untuk akurasi sebelum dikonversi ke uint8
            gray = (0.299 * self.Image[:, :, 0] +
                    0.587 * self.Image[:, :, 1] +
                    0.114 * self.Image[:, :, 2]).astype(np.uint8)
        else:
            # Jika sudah grayscale
            gray = self.Image.copy()

        self.Image = gray
        self.Image_ori = self.Image  # Simpan sebagai citra asli baru
        self.displayImage(2)  # Tampilkan hasil grayscale di label hasil

    # Fungsi untuk mengubah menjadi biner
    def biner(self):
        if self.Image is None:
            QMessageBox.warning(self, "Error", "Belum ada citra yang dimuat.")
            return
        H, W = self.Image.shape[:2]  # untuk mengambil ukuran gambar
        threshold = 180
        for i in range(H):  # iterasi untuk setiap pixel baris (tinggi)
            for j in range(W):  # iterasi untuk setiap pixel kolom (lebar)
                a = self.Image.item(i, j)  # untuk mengambil nilai pixel pada image
                if a < threshold:
                    b = 0
                else:
                    b = 255

                self.Image.itemset((i, j),
                                   b)  # untuk mengubah nilai pixel (i, j) menjadi b(b itu adalah variabel yang menyimpan nilai pixel baru)
        self.displayImage(2)

    def brightness(self):
        try:
            # Mengubah citra ke grayscale jika belum dalam format grayscale
            self.Image = cv2.cvtColor(self.Image, cv2.COLOR_BGR2GRAY)
        except:
            # Jika gambar sudah grayscale atau terjadi error, lanjutkan tanpa mengubah
            pass

        # Mendapatkan tinggi (H) dan lebar (W) dari citra
        H, W = self.Image.shape[:2]

        # Menentukan nilai peningkatan kecerahan
        brightness = 80

        # Melakukan iterasi untuk setiap piksel dalam citra
        for i in range(H):
            for j in range(W):
                # Mengambil nilai intensitas piksel pada posisi (i, j)
                a = self.Image.item(i, j)
                # Menambahkan nilai brightness dan memastikan hasilnya berada dalam rentang 0–255
                b = np.clip(a + brightness, 0, 255)
                # Menetapkan nilai piksel baru setelah ditingkatkan kecerahannya
                self.Image[i, j] = b

        # Menampilkan citra hasil setelah peningkatan kecerahan
        self.displayImage(2)

    def contrast(self):
        # Coba konversi gambar ke grayscale jika masih dalam format berwarna
        try:
            self.Image = cv2.cvtColor(self.Image, cv2.COLOR_BGR2GRAY)
        except:
            pass  # Jika gambar sudah grayscale, abaikan error

        # Ambil tinggi dan lebar gambar
        H, W = self.Image.shape[:2]

        # Nilai pengali untuk meningkatkan kontras
        contrast = 1.7

        # Loop melalui setiap piksel
        for i in range(H):
            for j in range(W):
                a = self.Image.item(i, j)  # Ambil nilai piksel pada posisi (i, j)
                b = np.clip(a * contrast, 0, 255)  # Tingkatkan nilai piksel dan batasi antara 0–255

                self.Image[i, j] = b  # Simpan kembali ke gambar

        # Tampilkan gambar hasil kontras pada label hasil (mode 2)
        self.displayImage(2)

    def sharpening(self):
        # Cek apakah gambar sudah dimuat
        if self.Image is None:
            QMessageBox.warning(self, "Error", "Belum ada citra yang dimuat.")
            return

        # Periksa apakah gambar sudah dalam format grayscale
        if len(self.Image.shape) == 2:
            # Jika sudah grayscale, langsung gunakan
            image_to_sharpen = self.Image
        else:
            # Jika gambar masih berwarna, konversi ke grayscale
            image_to_sharpen = cv2.cvtColor(self.Image, cv2.COLOR_BGR2GRAY)

        # Definisikan kernel untuk sharpening (penajaman citra)
        kernel = np.array([[0, -1, 0],
                           [-1, 5, -1],
                           [0, -1, 0]])

        # Terapkan kernel pada citra dengan operasi filter 2D
        sharpened = cv2.filter2D(image_to_sharpen, -1, kernel)

        # Simpan hasil sebagai citra utama
        self.Image = sharpened
        self.Image_ori = self.Image  # Simpan juga sebagai image original baru
        self.displayImage(2)  # Tampilkan hasil sharpening di antarmuka

    # Mengubah gambar malam menjadi seperti siang
    def simulate_day(self):
        if self.Image is None:
            QMessageBox.warning(self, "Error", "Belum ada citra yang dimuat.")
            return

        # Mengubah tipe data ke float32 agar perhitungan lebih akurat
        self.Image = self.Image.astype(np.float32)

        # Langkah 1: Meningkatkan kecerahan gambar
        self.Image *= 1.5  # Menambah tingkat kecerahan sebesar 1.5 kali

        # Langkah 2: Meningkatkan kontras secara halus
        self.Image = (self.Image - 127) * 1.1 + 127  # Penyesuaian kontras terhadap titik tengah intensitas

        # Langkah 3: Menambahkan nuansa hangat — hanya diterapkan jika citra berformat RGB (3 kanal warna)
        if len(self.Image.shape) == 3 and self.Image.shape[2] == 3:
            self.Image[:, :, 0] *= 0.9  # Mengurangi intensitas warna biru
            self.Image[:, :, 1] *= 1.1  # Meningkatkan intensitas warna hijau
            self.Image[:, :, 2] *= 1.2  # Meningkatkan intensitas warna merah

        # Membatasi nilai piksel dalam rentang [0, 255] dan mengubah kembali ke tipe uint8
        self.Image = np.clip(self.Image, 0, 255).astype(np.uint8)

        # Menyimpan hasil transformasi dan menampilkan citra yang telah diubah
        self.Image_ori = self.Image
        self.displayImage(2)

    def smoothing(self):
        # Cek apakah gambar sudah dimuat
        if self.Image is None:
            QMessageBox.warning(self, "Error", "Belum ada citra yang dimuat.")
            return

        # Pastikan gambar dalam format grayscale
        if len(self.Image.shape) == 3:
            img = cv2.cvtColor(self.Image, cv2.COLOR_BGR2GRAY)  # Konversi ke grayscale jika gambar berwarna
        else:
            img = self.Image  # Jika sudah grayscale, langsung gunakan

        height, width = img.shape  # Ambil ukuran gambar

        # Siapkan gambar kosong untuk menyimpan hasil smoothing
        output = np.zeros((height, width), dtype=np.uint8)

        # Definisikan kernel mean filter 3x3 (rata-rata dari 9 elemen)
        kernel = np.array([
            [1, 1, 1],
            [1, 1, 1],
            [1, 1, 1]
        ], dtype=np.float32) / 9

        # Iterasi setiap piksel gambar kecuali bagian tepi
        for y in range(1, height - 1):
            for x in range(1, width - 1):
                # Ambil blok 3x3 piksel di sekitar titik (x, y)
                block = img[y - 1:y + 2, x - 1:x + 2]

                # Lakukan operasi konvolusi manual antara blok dan kernel
                value = np.sum(block * kernel)

                # Simpan hasilnya ke gambar output
                output[y, x] = int(value)

        # Perbarui self.Image dengan gambar hasil smoothing
        self.Image = output
        self.Image_ori = self.Image  # Simpan juga sebagai image original baru
        self.displayImage(2)  # Tampilkan hasil smoothing di antarmuka

    def equalization(self):
        # Cek apakah citra sudah dimuat atau belum
        if self.Image is None:
            QMessageBox.warning(self, "Error", "Belum ada citra yang dimuat.")
            return

        # Hitung histogram dari citra
        # np.histogram menghasilkan 2 array: hist (frekuensi) dan bins (rentang nilai)
        hist, bins = np.histogram(self.Image.flatten(), 256, [0, 256])

        # Hitung fungsi distribusi kumulatif (CDF)
        cdf = hist.cumsum()

        # Normalisasi CDF hanya untuk visualisasi (tidak digunakan untuk transformasi)
        cdf_normalized = cdf * hist.max() / cdf.max()

        # Masking nilai nol agar tidak menyebabkan pembagian oleh nol saat normalisasi CDF
        cdf_m = np.ma.masked_equal(cdf, 0)

        # Hitung rumus equalization:
        # Normalisasi CDF untuk rentang [0, 255] sesuai dengan intensitas 8-bit
        cdf_m = (cdf_m - cdf_m.min()) * 255 / (cdf_m.max() - cdf_m.min())

        # Ganti nilai-nilai yang di-mask (nol) dengan nol kembali
        cdf = np.ma.filled(cdf_m, 0).astype('uint8')

        # Transformasi citra menggunakan nilai CDF hasil normalisasi
        self.Image = cdf[self.Image]

        # Simpan hasil transformasi ke variabel Image_ori (jika diperlukan)
        self.Image_ori = self.Image

        # Tampilkan citra hasil transformasi
        self.displayImage(2)

        # Visualisasi hasil:
        # 1. Plot CDF yang sudah dinormalisasi (garis biru)
        # 2. Histogram dari citra hasil equalization (warna merah)
        plt.plot(cdf_normalized, color='b')
        plt.hist(self.Image.flatten(), 256, [0, 256], color='r')

        # Cetak nilai-nilai CDF dan histogram ke konsol
        print("== Histogram ==")
        print(cdf_normalized)
        print("== CDF ==")
        print(self.Image.flatten())

        # Atur tampilan grafik
        plt.xlim([0, 256])
        plt.legend(('cdf', 'histogram'), loc='upper left')
        # plt.show()

    def update_image(self):
        if self.Image_ori is None:
            return

        if self.Image is None:
            QMessageBox.warning(self, "Error", "Belum ada citra yang dimuat.")
            return

        # Get values from sliders
        brightness = self.slider_brightness.value()
        contrast = self.slider_contrast.value()

        # Start from original
        img = self.Image_ori.astype(np.float32)

        # Apply brightness
        img += brightness

        # Apply contrast
        img = (img - 127) * (1 + contrast / 100.0) + 127

        # Final clip and convert
        img = np.clip(img, 0, 255).astype(np.uint8)

        self.Image = img
        self.displayImage(mode=2)

    def imgReset(self):
        if self.Image is None:
            QMessageBox.warning(self, "Error", "Belum ada citra yang dimuat.")
            return
        self.Image = self.Image_reset
        self.Image_ori = self.Image_reset
        self.displayImage(mode=2)

    # Fungsi untuk menampilkan citra pada GUI
    def displayImage(self, mode=1):
        qformat = QImage.Format_Indexed8

        if len(self.Image.shape) == 3:
            if (self.Image.shape[2]) == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888

        img = QImage(self.Image, self.Image.shape[1], self.Image.shape[0],
                     self.Image.strides[0], qformat)
        img = img.rgbSwapped()
        pix = QPixmap.fromImage(img)

        if mode == 1:
            scaled_pix = pix.scaled(self.citra_Asli.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.citra_Asli.setPixmap(scaled_pix)
            self.citra_Asli.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            # self.citra_Asli.setPixmap(QPixmap.fromImage(img))
        elif mode == 2:
            scaled_pix = pix.scaled(self.citra_hasil.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.citra_hasil.setPixmap(scaled_pix)
            self.citra_hasil.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            # self.citra_hasil.setPixmap(QPixmap.fromImage(img))

    def DeteksiManusia(self):
        hog = cv2.HOGDescriptor()
        hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
        self.Image = imutils.resize(self.Image, width=min(400, self.Image.shape[0]))

        (regions, _) = hog.detectMultiScale(self.Image, winStride=(4, 4), padding=(4, 4), scale=1.05)

        for (x, y, w, h) in regions:
            cv2.rectangle(self.Image, (x, y), (x + w, y + h), (0, 0, 255), 2)

        self.displayImage(2)  # Display the original image with detections


app = QtWidgets.QApplication(sys.argv)
window = ShowImage()
window.setWindowTitle('High Light - Perbaikan Citra Gelap')
window.show()
sys.exit(app.exec_())