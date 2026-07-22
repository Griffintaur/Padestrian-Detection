# -*- coding: utf-8 -*-
"""

@author: Ankit Singh
"""

from ImageHandler import Imagehandler
from svmFile import svmClass
from utility import Pyramid, SlidingWindow
import yaml
import glob
import os
import random
import cv2 as cv


WINDOW_HEIGHT = 160
WINDOW_WIDTH = 96


def _image_paths(directory, file_types):
    paths = []
    for filetype in file_types:
        paths.extend(glob.glob(os.path.join(directory, "*." + filetype)))
    return paths


def App():
    base_dir = os.path.dirname(os.path.abspath(__file__))

    with open(os.path.join(base_dir, "config.yml"), 'r') as ymlfile:
        cfg = yaml.safe_load(ymlfile)

    IOPlaces = cfg['Main']
    inputs = IOPlaces['Input']
    output = IOPlaces['Output']
    directorypathpos = os.path.join(base_dir, inputs['positive'])
    directorypathneg = os.path.join(base_dir, inputs['Negative'])
    outputpath = os.path.join(base_dir, output)
    filesTypes = cfg['FileType']
    DataX = []
    DataY = []

###adding and Computing HOG Vector
    #image sizez are 96* 160

    for path in _image_paths(directorypathpos, filesTypes):
        obj = Imagehandler(path)
        HogVector = obj.ImagesToTiles(16, 16)
        DataX.append(HogVector)
        DataY.append(1)

    for path in _image_paths(directorypathneg, filesTypes):
        Image = cv.imread(path, cv.IMREAD_UNCHANGED)
        if Image is None:
            continue

        imageHeight, imageWidth = Image.shape[:2]
        if imageHeight < WINDOW_HEIGHT or imageWidth < WINDOW_WIDTH:
            continue

        for _ in range(10):
            y = random.randint(0, imageHeight - WINDOW_HEIGHT)
            x = random.randint(0, imageWidth - WINDOW_WIDTH)
            img = Image[y:y + WINDOW_HEIGHT, x:x + WINDOW_WIDTH]
            obj = Imagehandler(path, img)
            HogVector = obj.ImagesToTiles(16, 16)
            DataX.append(HogVector)
            DataY.append(0)

    if len(set(DataY)) < 2:
        raise ValueError("Training requires at least one positive and one negative sample")

###train and test

    svmObj = svmClass((DataX,DataY))
    svmObj.trainData()


####predict
    for path in _image_paths(outputpath, filesTypes):
        Image = cv.imread(path, cv.IMREAD_UNCHANGED)
        if Image is None:
            continue

        imageHeight,imageWidth = Image.shape[:2]
        imageHeight = int(imageHeight / WINDOW_HEIGHT) * WINDOW_HEIGHT
        imageWidth = int(imageWidth / WINDOW_WIDTH) * WINDOW_WIDTH
        if imageHeight < WINDOW_HEIGHT or imageWidth < WINDOW_WIDTH:
            continue

        Image  =  cv.resize(Image,(imageWidth,imageHeight), interpolation  =  cv.INTER_CUBIC)
        detections = []
        for scaledImage in Pyramid(Image, 2, (128, 64)):
            for (x, y, window) in SlidingWindow(scaledImage, (14, 14), (WINDOW_HEIGHT, WINDOW_WIDTH)):
                if window.shape[:2] != (WINDOW_HEIGHT, WINDOW_WIDTH):
                    continue
                oi = Imagehandler(path, window)
                Hog = oi.ImagesToTiles(16, 16)
                val = svmObj.PredictData([Hog])
                val =  val[0]
                print(val)
                if val[1]> 0.8:
                    detections.append((scaledImage, x, y))

        for scaledImage, x, y in detections:
            clone = scaledImage.copy()
            cv.rectangle(clone, (x, y), (x + WINDOW_WIDTH, y + WINDOW_HEIGHT), (0, 255, 0), 2)
            cv.imshow("Window", clone)
            cv.waitKey(1)


if __name__  ==  "__main__":

    cam = cv.VideoCapture(0)
    App()
    cam.release()
    cv.destroyAllWindows()
