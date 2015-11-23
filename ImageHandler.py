# -*- coding: utf-8 -*-
"""

@author: Ankit Singh
"""

import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import os

class Imagehandler(object):
    def __init__(self,path):
        if (os.path.exists(path) and os.path.isfile(path)):
            self.ImagePath=path
            self.Image=cv.imread(self.ImagePath,cv.IMREAD_COLOR)
        else:
            print "file not found"
    
    def __convertImagetoBlackWhite(self):
        self.Image=cv.imread(self.ImagePath,cv.IMREAD_COLOR)
        self.imageOriginal=self.Image
        if(self.Image is None):
            print "some problem with the image"
        else:
            print "Image Loaded"
            
        self.Image=cv.cvtColor(self.Image,cv.COLOR_BGR2GRAY)
        self.Image=cv.adaptiveThreshold(self.Image,255,cv.ADAPTIVE_THRESH_MEAN_C,cv.THRESH_BINARY,11,2)
        return self.Image
    
    def WritingImage(self,image,path,imageName):
        if(image is None):
            print"Image is not valid.Please select some other image"
        else:
            image=cv.cvtColor(image,cv.COLOR_BGR2RGB)
            print path+imageName
            cv.imwrite(path+imageName,image)
            cv.imshow(imageName,image)
            cv.waitKey(0);

    def GetGradients(self):
        gradientX=cv.Sobel(self.Image,cv.CV_64F,1,0,ksize=1)
        gradientY=cv.Sobel(self.Image,cv.CV_64F,1,0,ksize=1)
        NormalizingConstant=np.sqrt(np.sum(gradientX**2+ gradientY**2))
        gradientX=gradientX/NormalizingConstant
        gradientY=gradientY/NormalizingConstant
        return (gradientX,gradientY)
    
    def ConvertToPolarForm(self,gradients):
        gradientX,gradientY=gradients
        mag,angle=cv.cartToPolar(gradientX,gradientY,angleInDegrees=True)
        return (mag,angle)
    
    def ImagesToTiles(self,tileX,tileY):
        imageHeight,imageWidth=self.Image.shape[:2]
        imageHeight=int(imageHeight/tileY)*tileY
        imageWidth=int(imageWidth/tileX)*tileX
        self.Image = cv.resize(self.Image,(imageWidth,imageHeight), interpolation = cv.INTER_CUBIC)
        #cv.resize takes shape as (width,height) instead of height,width
        print imageHeight,imageWidth
        print self.Image.shape
        i=0
        j=0
        while i<= imageHeight:
            j=0
            while j <= imageWidth:
                img=self.Image[j:j+tileY,i:i+tileX]
                print i,j,i+tileX,j+tileY
                cv.rectangle(self.Image,(j,i), (j+tileY,i+tileX), (0,255,0),3)
#                cv.waitKey(0)
#                print j,i
        
                j=j+tileY
            print "increase x"
            i=i+tileX
        cv.rectangle(self.Image,(0,0), (200,200), (255,0,0),3)
        cv.rectangle(self.Image,(0,200), (200,400), (255,0,0),3)
        cv.imshow("hi",self.Image)
        cv.waitKey(0)
            

        
    
        