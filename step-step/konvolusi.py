import numpy as np
from scipy.ndimage import convolve

# Definisikan citra input 10x10
image = np.array([
    [165, 171, 179, 199, 191, 185, 124, 112, 203, 203],
    [99, 159, 183, 212, 143, 162, 174, 123, 185, 171],
    [180, 181, 147, 215, 126, 184, 135, 88, 172, 205],
    [166, 180, 120, 160, 211, 164, 206, 114, 188, 196],
    [99, 166, 160, 133, 154, 174, 161, 99, 97, 182],
    [177, 160, 164, 166, 120, 169, 178, 97, 123, 203],
    [181, 170, 183, 182, 150, 66, 159, 128, 156, 178],
    [179, 155, 115, 179, 148, 109, 114, 98, 98, 192],
    [116, 164, 179, 179, 112, 141, 198, 98, 98, 153],
    [159, 180, 141, 176, 161, 116, 129, 120, 164, 140]
])

# Kernel Sobel horizontal dan vertikal
sobel_x = np.array([[1, 0, -1],
                    [2, 0, -2],
                    [1, 0, -1]])
sobel_y = np.array([[1, 2, 1],
                    [0, 0, 0],
                    [-1, -2, -1]])

# Konvolusi
gradient_x = convolve(image, sobel_x)
gradient_y = convolve(image, sobel_y)

# Hitung magnitudo dan arah (derajat)
magnitude = np.sqrt(gradient_x**2 + gradient_y**2)
direction = np.arctan2(gradient_y, gradient_x) * (180 / np.pi)

# Potong hasil menjadi 8x8
magnitude = magnitude[1:-1, 1:-1]
direction = direction[1:-1, 1:-1]

# Fungsi mencetak array float dengan 2 desimal, format seperti array NumPy
def print_array_float(array, name):
    print(f"{name}:\narray([")
    for row in array:
        formatted_row = ", ".join(f"{val:.2f}" for val in row)
        print(f"    [{formatted_row}],")
    print("])")

# Print hasil
print_array_float(magnitude, "Magnitudo Deteksi Tepi")
print_array_float(direction, "Arah Tepi (derajat)")
