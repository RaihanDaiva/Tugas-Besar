import sys
import cv2
import numpy as np
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from matplotlib import pyplot as plt

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
        self.button_Brightness.clicked.connect(self.brightness)
        self.button_Contrast.clicked.connect(self.contrast)
        self.button_Sharpening.clicked.connect(self.sharpening)
        self.button_simulateDay.clicked.connect(self.simulate_day)
        self.button_Smoothing.clicked.connect(self.smoothing)
        self.actionEqualization.triggered.connect(self.equalization)

        self.slider_brightness.setMinimum(-100)
        self.slider_brightness.setMaximum(100)
        self.slider_brightness.setValue(0)  # Default = no brightness change
        self.slider_brightness.valueChanged.connect(self.update_image)

        self.slider_contrast.setMinimum(-100)
        self.slider_contrast.setMaximum(100)
        self.slider_contrast.setValue(0)  # Default = no brightness change
        self.slider_contrast.valueChanged.connect(self.update_image)


    #Fungsi untuk membaca citra
    def load(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Pilih Gambar", "", "Image Files (*.png *.jpg *.jpeg *.bmp)")

        if file_name:
            self.Image = cv2.imread(file_name)
            self.Image_ori = self.Image
            if self.Image is None:
                QMessageBox.warning(self, "Error", "Gagal membaca gambar.")
                return
            self.displayImage(1)
    
    #Fungsi untuk menyimpan citra hasil
    def saveHasil(self):
        if self.Image is None:
            QMessageBox.warning(self, "Error", "Belum ada citra yang dimuat atau diolah.")
            return
        
        success = cv2.imwrite('Citra_Hasil.jpg', self.Image)
        if success:
            QMessageBox.information(self, "Berhasil", "Citra berhasil disimpan sebagai 'Citra_Hasil.jpg'.")
        else:
            QMessageBox.warning(self, "Gagal", "Gagal menyimpan citra.")
    
    #Fungsi untuk menyimpan citra asli
    def saveAsli(self):
        if self.Image is None:
            QMessageBox.warning(self, "Error", "Belum ada citra yang dimuat.")
            return
        
        success = cv2.imwrite('Citra_Asli.jpg', self.Image)
        if success:
            QMessageBox.information(self, "Berhasil", "Citra berhasil disimpan sebagai 'Citra_Asli.jpg'.")
        else:
            QMessageBox.warning(self, "Gagal", "Gagal menyimpan citra.")
    
    #Fungsi untuk mengubah menjadi grayscale
    def grayscale(self):
        H, W = self.Image.shape[:2]
        gray = np.zeros((H, W), np.uint8)
        for i in range (H):
            for j in range (W):
                gray[i, j] = np.clip(0.299 * self.Image[i, j, 0] +
                                     0.587 * self.Image[i, j, 1] +
                                     0.114 * self.Image[i, j, 2], 0, 255)
        self.Image = gray
        self.displayImage(2)
        
    #Fungsi untuk mengubah menjadi biner
    def biner(self):
        H, W = self.Image.shape[:2] #untuk mengambil ukuran gambar
        threshold = 180
        for i in range (H): #iterasi untuk setiap pixel baris (tinggi)
            for j in range (W): #iterasi untuk setiap pixel kolom (lebar)
                a = self.Image.item(i, j)  #untuk mengambil nilai pixel pada image
                if a < threshold:
                    b = 0
                else:
                    b = 255
                
                self.Image.itemset((i, j), b)   #untuk mengubah nilai pixel (i, j) menjadi b(b itu adalah variabel yang menyimpan nilai pixel baru) 
        self.displayImage(2)

    def brightness(self):
        try:
            self.Image = cv2.cvtColor(self.Image, cv2.COLOR_BGR2GRAY)
        except:
            pass
        H, W = self.Image.shape[:2]
        brightness = 80
        for i in range(H):
            for j in range(W):
                a = self.Image.item(i, j)
                b = np.clip(a + brightness, 0, 255)

                self.Image[i, j] = b

        self.displayImage(2)

    def contrast(self):
        try:
            self.Image = cv2.cvtColor(self.Image, cv2.COLOR_BGR2GRAY)
        except:
            pass
        H, W = self.Image.shape[:2]
        contrast = 1.7
        for i in range(H):
            for j in range(W):
                a = self.Image.item(i, j)
                b = np.clip(a * contrast, 0, 255)

                self.Image[i, j] = b

        self.displayImage(2)

    def sharpening(self):
        if self.Image is None:
            QMessageBox.warning(self, "Error", "Belum ada citra yang dimuat.")
            return

        if len(self.Image.shape) == 2:
            # Citra sudah grayscale
            image_to_sharpen = self.Image
        else:
            # Jika masih berwarna, konversi dulu ke grayscale
            image_to_sharpen = cv2.cvtColor(self.Image, cv2.COLOR_BGR2GRAY)

            # Kernel sharpening
        kernel = np.array([[0, -1, 0],
                           [-1, 5, -1],
                           [0, -1, 0]])

        sharpened = cv2.filter2D(image_to_sharpen, -1, kernel)
        self.Image = sharpened
        self.Image_ori = self.Image
        self.displayImage(2)

    # Mengubah gambar malam menjadi seperti siang
    def simulate_day(self):
        # Convert to float32 for better math
        self.Image = self.Image.astype(np.float32)

        # Step 1: Brighten the image
        self.Image *= 1.5  # Increase brightness

        # Step 2: Slightly increase contrast
        self.Image = (self.Image - 127) * 1.1 + 127

        # Step 3: Add warmth — only if the image is RGB (i.e., 3 channels)
        if len(self.Image.shape) == 3 and self.Image.shape[2] == 3:
            self.Image[:, :, 0] *= 0.9  # Reduce blue
            self.Image[:, :, 1] *= 1.1  # Boost green
            self.Image[:, :, 2] *= 1.2  # Boost red

        # Clip values to [0, 255] and convert back to uint8
        self.Image = np.clip(self.Image, 0, 255).astype(np.uint8)
        self.displayImage(2)
        
    def smoothing(self):
        if self.Image is None:
            QMessageBox.warning(self, "Error", "Belum ada citra yang dimuat.")
            return

        # Pastikan gambar dalam format grayscale
        if len(self.Image.shape) == 3:
            img = cv2.cvtColor(self.Image, cv2.COLOR_BGR2GRAY)
        else:
            img = self.Image

        height, width = img.shape

        # Siapkan gambar hasil smoothing
        output = np.zeros((height, width), dtype=np.uint8)

        # Definisikan kernel 3x3 mean filter
        kernel = np.array([
            [1, 1, 1],
            [1, 1, 1],
            [1, 1, 1]
        ], dtype=np.float32) / 9  # rata-rata

        # Looping untuk tiap piksel (kecuali tepi)
        for y in range(1, height - 1):
            for x in range(1, width - 1):
                # Ambil blok 3x3 dari gambar asli
                block = img[y-1:y+2, x-1:x+2]

                # Hitung hasil konvolusi manual
                value = np.sum(block * kernel)
                
                # Simpan ke gambar hasil
                output[y, x] = int(value)

        # Perbarui self.Image dengan hasil smoothing
        self.Image = output
        self.Image_ori = self.Image
        self.displayImage(2)

    def equalization(self):
        hist, bins = np.histogram(self.Image.flatten(), 256, [0, 256])
        cdf = hist.cumsum()
        cdf_normalized = cdf * hist.max() / cdf.max()
        cdf_m = np.ma.masked_equal(cdf, 0)
        cdf_m = (cdf_m - cdf_m.min()) * 255 / (cdf_m.max() - cdf_m.min())
        cdf = np.ma.filled(cdf_m, 0).astype('uint8')
        self.Image = cdf[self.Image]
        self.displayImage(2)

        plt.plot(cdf_normalized, color='b')
        plt.hist(self.Image.flatten(), 256, [0, 256], color='r')
        plt.xlim([0, 256])
        plt.legend(('cdf', 'histogram'), loc='upper left')
        plt.show()

    def update_image(self):
        if self.Image_ori is None:
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
        
    #Fungsi untuk menampilkan citra pada GUI
    def displayImage(self, mode=1):
        qformat = QImage.Format_Indexed8

        if len(self.Image.shape)==3:
            if(self.Image.shape[2])==4:
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
            
app = QtWidgets.QApplication(sys.argv)
window = ShowImage()
window.setWindowTitle('Pertemuan 1')
window.show()
sys.exit(app.exec_())