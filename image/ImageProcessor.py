import cv2
import numpy as np
import sys, select, os


def gray(img):
    imgArray = np.array(img)
    im_gray = 0.299 * img[:, :, 0] + 0.587 * img[:, :, 1] + 0.114 * img[:, :, 2]
    # for width in range(img.shape[0]):
    #     for height in range(img.shape[1]):
    #         pixdata = imgArray[width][height]
    #         y = 0.229 * pixdata[0] + 0.587 * pixdata[1] + 0.114 * pixdata[2]
    #         img[width, height] = y
    #         # img.itemset((width, height, 0), y)
    #         # img.itemset((width, height, 1), y)
    #         # img.itemset((width, height, 2), y)
    return im_gray

def binary(img):
    imgArray = np.array(img)
    return img

def negative(img):
    imgArray = np.array(img)
    return img

def mosaic(img):
    imgArray = np.array(img)
    return img

cam = cv2.VideoCapture(0)
key = -1

while True:
    _, img = cam.read()

    if key == int(ord('q')):
        break
    elif key == int(ord('1')):
        img = gray(img)
    elif key == int(ord('2')):
        img = binary(img)
    elif key == int(ord('3')):
        img = negative(img)
    elif key == int(ord('4')):
        img = mosaic(img)
    elif key == int(ord('5')):
        img = gray(img)
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
