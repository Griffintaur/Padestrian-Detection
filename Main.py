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

def App():
    with open("config.yml", 'r') as ymlfile:
        cfg = yaml.load(ymlfile)
    IOPlaces=cfg['Main']
    input=IOPlaces['Input']
    output=IOPlaces['Output']
    print output
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
    #image sizez are 96* 160
    
    for i in xrange(len(paths)):
        Image=cv.imread(paths[i],cv.IMREAD_COLOR)
        obj=Imagehandler(paths[i])
        HogVector=obj.ImagesToTiles(16,16)
        DataX.append(HogVector)
        DataY.append(1)
        
    directorypathneg=input['negative']
    os.chdir(directorypathneg)
    images=[]
    for filetype in filesTypes:
        images.extend(glob.glob("*."+filetype))
    paths=[directorypathneg+image for image in images]
#   print xrange(len(paths))
    for i in xrange(len(paths)):
        Image=cv.imread(paths[i],cv.IMREAD_COLOR)
        for j in xrange(10):
            rand=random.randomrange(0,50)
            img=Image[rand:rand+96,rand:rand+160]
            obj=Imagehandler(paths[i],img)
            HogVector=obj.ImagesToTiles(16,16)
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
    paths=[directorypathneg+image for image in images]
    for i in xrange(len(paths)):
        Image=cv.imread(paths[i],cv.IMREAD_COLOR)
        for scaledImage in Pyramid(Image,1.25,(60,60)):
            for (x,y,window) in SlidingWindow(scaledImage,(4,4),(64,128)):
                oi=Imagehandler(paths[i],window)
                Hog=oi.ImageToTiles(16,16)
                val=svmObj.PredictData(Hog)
                if val> 0.5:
                    clone = scaledImage.copy()
                    cv.rectangle(clone, (x, y), (x + 64, y + 128), (0, 255, 0), 2)
                    cv.imshow("Window", clone)
                    cv.waitKey(1)
 

if __name__ == "__main__":
    
    cam = cv.VideoCapture(0)
    App()
    cam.release()
    cv.destroyAllWindows()