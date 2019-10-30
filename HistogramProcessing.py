# -*- coding: utf-8 -*-
"""

@author: Ankit Singh
"""
import cv2 as cv
import numpy as np

class HistogramOperations(object):
    def __init__(self, image):
        self.Image = image
        self.ImageHeight, self.ImageWidth = image[:2]
        self.Maxangle = 180

    def CreateHistogram(self, channel):
#        hist=cv.calcHist(self.Image, channel, mask, histSize, range)
        pass

    def GetGradients(self):
        gradient_x = cv.Sobel(self.Image, cv.CV_64F, 1, 0, ksize=1)
        gradient_y = cv.Sobel(self.Image, cv.CV_64F, 1, 0, ksize=1)
#        NormalizingConstant = np.sqrt(np.sum(gradient_x*gradient_x+ gradient_y*gradient_y))
#        gradient_x = gradient_x/(NormalizingConstant +1e-10)
#        gradient_y = gradient_y/(NormalizingConstant +1e-10)
        return (gradient_x, gradient_y)

    def ConvertToPolarForm(self, gradients):
        gradient_x, gradient_y = gradients
        mag, angle = cv.cartToPolar(gradient_x, gradient_y, angleInDegrees=True)
        return (mag.flatten(), angle.flatten())
        #these things are not needed in the case of the PNG images and are only needed in case of three Channels
        #such as RGB Images.

#        tempImageTilemag = []
#        tempImageTileangle = []
#        for tile in mag:
#            temptile = []
#            temptileang = []
#            if len(tile) == 3:
#                for pixel in tile:
#                    print pixel
#                    temp=np.argmax(pixel)
#                    print temp, pixel.shape
#                    temptile.append(pixel[temp])
#                    temptileang.append(pixel[temp])
#            else:
#                temptile.append(pixel)
#                temptileang.append(pixel[temp])
#            tempImageTilemag.append(temptile)
#            tempImageTileangle.append(temptileang)
#        flat_list_mag = []
#        flat_list_ang = []
#        for sublist in tempImageTilemag:
#            for item in sublist:
#                flat_list_mag.append(item)
#        for sublist in tempImageTileangle:
#            for item in sublist:
#                flat_list_ang.append(item)
#        tempImageTileangle = np.reshape(np.array(tempImageTilemag), (self.ImageHeight, self.ImageWidth))
#        tempImageTileangle = np.reshape(np.array(tempImageTileangle), (self.ImageHeight, self.ImageWidth))
#        return (flat_list_mag, flat_list_ang)

    def HistogramOfGradient(self, image, noofbins):
        gradient_x, gradient_y = self.GetGradients()
#        print gradient_x, gradient_y
        mag_gradient_list, angle_gradient_list = self.ConvertToPolarForm((gradient_x, gradient_y))
#        print mag_gradient_list
        bins = [0.0]*noofbins #nine bind [0,20,40,60,80,100,120,140,160]
        offset = int(self.Maxangle/noofbins) #this should be divisble for more accuracy
        #print angle_gradient_list
        #print mag_gradient_list
        for i, angle_gradient in enumerate(angle_gradient_list):
            if angle_gradient > 180:
                angle_gradient = angle_gradient-180
            left_bin = int(angle_gradient/offset)
            left_bin = left_bin%noofbins
            right_bin = left_bin+1 if left_bin != noofbins-1 else 0
            right_ratio = (angle_gradient-left_bin*offset)/offset
#            print right_ratio
            left_ratio = 1-right_ratio
#            print left_bin,right_bin
            if left_ratio < 0  or right_ratio < 0:
                print(right_ratio, angle_gradient, left_bin)
                print("wait")
            bins[left_bin] = mag_gradient_list[i]*left_ratio
            bins[right_bin] = mag_gradient_list[i]*right_ratio
#        print( bins)
        return bins
    def ConcatAndNormalisationofHistogram(self, histogramList):
        feature_vector = []
#        print "lol",histogramList
        for i, tempHistogramList in enumerate(histogramList):
            for histogram in tempHistogramList:
                feature_vector.append(histogram)
        norm_sum = sum(hist*hist for hist in feature_vector)
#        print "suck",feature_vector
        feature_vector = [feature/(norm_sum+1e-10) for feature in feature_vector]
        #print "fuck",feature_vector
        return feature_vector
    @staticmethod
    def ConcatFeatureVectors(vectors):
        image_vector = []
        #print "done"
        for i in xrange(len(vectors)):
            tempvectors = vectors[i]
            [image_vector.append(vector)for vector in tempvectors]
#        print ( len(image_vector))
        return image_vector
