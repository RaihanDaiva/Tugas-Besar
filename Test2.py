import cv2
import imutils

img = cv2.imread('DSC_0262.JPG')
img = imutils.resize(img, width=min(400, img.shape[0]))
img = cv2.imwrite('resizefix.jpg', img)