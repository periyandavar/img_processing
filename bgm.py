import numpy as np
import cv2

def fun(im,bgm):
   bgm=cv2.imread(bgm)
   height, width, channels = im.shape
   bgm = cv2.resize(bgm, (width,height), interpolation = cv2.INTER_AREA)
   gray  =   cv2.cvtColor(im,   cv2.COLOR_BGR2GRAY)
   ret,    mask    =   cv2.threshold(gray, 125,    255,    cv2.THRESH_BINARY)
   mask_inv    =   cv2.bitwise_not(mask)
   temp    =   cv2.bitwise_and(bgm,  bgm,  mask=mask)
   temp2   =   cv2.bitwise_and(im,   im,    mask=mask_inv)
   final_img   =   cv2.add(temp,   temp2)
   return final_img