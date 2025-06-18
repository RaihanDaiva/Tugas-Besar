import numpy as np
import matplotlib.pyplot as plt

# Data magnitude dan direction (arah sudut dalam derajat)
mag = np.array([
    [166.86, 106.32, 112.79, 171.45, 102.0, 106.68, 102.62, 193.38],
    [157.31, 127.58, 231.37, 207.71, 195.73, 174.13,  51.24,  63.07],
    [ 93.34, 119.64, 188.6,  164.98, 224.52, 233.83, 120.44, 122.59],
    [197.21, 130.21, 156.11, 112.18, 159.53, 262.07,  44.27,  24.04],
    [ 30.59, 259.26, 342.38, 233.85, 251.11, 256.03,  18.97,  56.14],
    [111.0, 281.4, 207.63, 103.24, 335.26, 206.89,  99.01,  93.68],
    [ 51.88, 284.31, 256.22, 121.8, 278.95, 203.96,  87.73,  35.61],
    [ 10.3, 151.42, 226.5,   73.88, 185.99, 202.41,  23.02,  44.72]
])

dir = np.array([
    [-115.18, -106.39, -165.1,  -163.04,  -28.07,   6.46, 105.26,  79.27],
    [-112.82,  -76.4,  -130.09, -128.75,   -7.63,  24.06, 107.02,  -2.73],
    [  45.0,  102.06,  143.19,  120.61,   18.43,  14.87, 119.33,  61.76],
    [  34.25, 126.25,  154.58,  168.69,    4.67,   1.31, 161.57, -73.07],
    [  11.31, -128.11, -122.11, -102.85,  -19.3,   -0.9, 161.57, 175.91],
    [ 169.09, -174.29, -159.12,   3.89,   17.35,  13.7, -135.82, -106.11],
    [-152.45, 158.76,  143.89,   29.51,  -17.53, -41.82, -136.85, -128.16],
    [ -60.95, 167.8,   150.95,  140.49,  -19.8,  -17.54,  -34.38, 116.57]
])

def compute_hog_cell_interpolated(direction, magnitude, bin_size=20):
    # Ubah semua sudut ke rentang [0, 180)
    direction = np.mod(direction, 180)

    bins = np.arange(0, 181, bin_size)  # contoh: [0, 20, ..., 180]
    histogram = np.zeros(len(bins) - 1)

    for i in range(direction.shape[0]):
        for j in range(direction.shape[1]):
            angle = direction[i, j]
            mag = magnitude[i, j]

            # Cari dua bin terdekat
            lower_bin = int(angle // bin_size)
            upper_bin = (lower_bin + 1) % len(histogram)

            lower_angle = bins[lower_bin]
            upper_angle = bins[upper_bin] if upper_bin > lower_bin else 180

            # Interpolasi linier
            weight_upper = (angle - lower_angle) / bin_size
            weight_lower = 1 - weight_upper

            histogram[lower_bin] += mag * weight_lower
            histogram[upper_bin] += mag * weight_upper

    return bins[:-1], histogram

# Hitung histogram HOG dengan interpolasi
bins, histogram = compute_hog_cell_interpolated(dir, mag)

# Plot histogram HOG
plt.figure(figsize=(8, 4))
plt.bar(bins, histogram, width=20, align='edge', edgecolor='black')
plt.xlabel('Orientasi Gradien (derajat)')
plt.ylabel('Magnitudo Gradien')
plt.title('Histogram HOG (Interpolated Binning)')
plt.xticks(bins)
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()
