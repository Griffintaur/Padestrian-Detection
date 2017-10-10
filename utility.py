#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 10 17:20:27 2017

@author: Ankit Singh
"""
import cv2 as cv

def Pyramid(img,scale,minsize):
    "this function is used to creeate the guassian pyramid of the images"
    yield img
    imageHeight,imageWidth=img.shape[:2]
    while (imageHeight,imageWidth) >minsize:
        imageHeight=int(imageHeight/scale)
        imageWidth=int(imageWidth/scale)
        img=cv.resize(img,(imageWidth,imageHeight), interpolation = cv.INTER_CUBIC)
        yield img
        
def SlidingWindow(image, stepSize, windowSize):
	for y in xrange(0, image.shape[0], stepSize):
		for x in xrange(0, image.shape[1], stepSize):
			yield (x, y, image[y:y + windowSize[1], x:x + windowSize[0]])      
        