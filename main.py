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
        self.button_Sharpening.clicked.connect(self.sharpening)
        
    #Fungsi untuk membaca citra
    def load(self):
        self.Image = cv2.imread('sample2.jpg')
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
        self.displayImage(2)
        
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