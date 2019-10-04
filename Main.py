# -*- coding: utf-8 -*-
"""

@author: Ankit Singh
"""

from ImageHandler import Imagehandler
from svmFile import svmClass
from utility import Pyramid,SlidingWindow
import yaml
import glob
import os
import random
import cv2 as cv
import Img_final

def App():
    with open("config.yml", 'r') as ymlfile:
        cfg = yaml.load(ymlfile)
    IOPlaces=cfg['Main']
    input=IOPlaces['Input']
    output=IOPlaces['Output']
#    print output
    directorypathpos=input['positive']
    os.chdir(directorypathpos)
    filesTypes=cfg['FileType']
    images=[]
    for filetype in filesTypes:
        images.extend(glob.glob("*."+filetype))
    DataX=[]
    DataY=[] 
    paths=[directorypathpos+image for image in images]
    
###adding and Computing HOG Vector
#   print xrange(len(paths))
    #image sizez are 96* 96 (updated)
    
    for i in xrange(len(paths)):
#    for i in xrange(100):
#        Image=cv.imread(paths[i],cv.IMREAD_COLOR)
        obj=Imagehandler(paths[i])
        HogVector=obj.ImagesToTiles(16,16)
        DataX.append(HogVector)
        DataY.append(1)
        
    directorypathneg=input['Negative']
    os.chdir(directorypathneg)
    images=[]
    for filetype in filesTypes:
        images.extend(glob.glob("*."+filetype))
    paths=[directorypathneg+image for image in images]
#   print xrange(len(paths))
    for i in xrange(len(paths)):
#    for i in xrange(10):
        Image=cv.imread(paths[i],cv.IMREAD_UNCHANGED)
        for j in xrange(10):
            rand=random.randint(0,50)
            img=Image[rand:rand+96,rand:rand+96]
            obj=Imagehandler(paths[i],img)
            HogVector=obj.ImagesToTiles(16,16)
#            print len(HogVector)
            DataX.append(HogVector)
            DataY.append(0)
    
   
    
 ###train and test   

    svmObj=svmClass((DataX,DataY))
    svmObj.trainData()
    
    
####predict 
    os.chdir(output)
    images=[]
    for filetype in filesTypes:
        images.extend(glob.glob("*."+filetype))
    paths=[output+image for image in images]
#    for i in xrange(len(paths)):
    for i in xrange(5):
        Image=cv.imread(paths[i],cv.IMREAD_UNCHANGED)
        imageHeight,imageWidth=Image.shape[:2]
        imageHeight=int(imageHeight/96)*96
        imageWidth=int(imageWidth/96)*96
        Image = cv.resize(Image,(imageWidth,imageHeight), interpolation = cv.INTER_CUBIC)
        for scaledImage in Pyramid(Image,2,(128,64)):
            for (x,y,window) in SlidingWindow(scaledImage,(14,14),(96,96)):
                if( window.shape[:2] != (160,96)):
                    continue
                oi=Imagehandler(paths[i],window)
                Hog=oi.ImagesToTiles(16,16)
#                print len(Hog)
                val=svmObj.PredictData([Hog])
                val= val[0]
                print val
                if val[1]> 0.85:
                    clone = scaledImage.copy()
                    cv.square(clone, (x, y), (x + 96, y + 96), (0, 255, 0), 2)
                    cv.imshow("Window", clone)
                    cv.waitKey(1)
 if Img_final!=NULL
 print val
#{cv.rectangle(clone,(x,y),(x+96,y+96), (0,255,0),2) removed for greater efficiency

if __name__ == "__main__":
    
    cam = cv.VideoCapture(0)
    App()
    cam.release()
    cv.destroyAllWindows()
