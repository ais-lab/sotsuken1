import cv2
import numpy as np
import sys, select, os


def gray(img):
    imgArray = np.asarray(img)
    imgArray = 0.299 * imgArray[:, :, 0] + 0.587 * imgArray[:, :, 1] + 0.114 * imgArray[:, :, 2]
    imgArray = imgArray.astype(np.uint8)
    return imgArray

def binary(img):
    imgArray = gray(img)
    thread = 100
    binary_img = (imgArray > thread) * 255
    binary_img = binary_img.astype(np.uint8)
    return binary_img

def negative(img):
    imgArray = np.asarray(img)
    imgArray = 255 - imgArray
    return imgArray

def mosaic(img):
    imgArray = np.asarray(img)
    for index in imgArray:
        print (index[0][0], index[0][1], index[0][2])
        print ("-----")
        
    return img

def rotation(img):
    imgArray = np.asarray(img)
    imgArray = imgArray[::-1]
    return imgArray


cam = cv2.VideoCapture(0)
key = -1

while True:
    _, img = cam.read()
    size = (img.shape[1]//2, img.shape[0]//2)
    img = cv2.resize(img, size)

    if key == int(ord('q')):
        break
    elif key == int(ord('1')):
        img = gray(img)
    elif key == int(ord('2')):
        img = binary(img)
    elif key == int(ord('3')):
        img = negative(img)
    elif key == int(ord('4')):
        img = rotation(img)
    elif key == int(ord('5')):
        img = mosaic(img)
    elif key == int(ord('6')):
        img = gray(img)
    else:
        pass

    cv2.imshow('Frame', img)
    input = cv2.waitKey(1)

    if input == -1:
        pass
    else:
        key = input

cam.release()
cv2.destroyAllWindows()
