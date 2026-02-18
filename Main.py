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


def App():

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    with open("config.yml", 'r') as ymlfile:
        cfg = yaml.safe_load(ymlfile)

    IOPlaces = cfg['Main']
    input_cfg = IOPlaces['Input']
    output_cfg = IOPlaces['Output']

    directorypathpos = os.path.join(BASE_DIR, input_cfg['positive'])
    directorypathneg = os.path.join(BASE_DIR, input_cfg['Negative'])
    output_path = os.path.join(BASE_DIR, output_cfg)

    filesTypes = cfg['FileType']

    DataX = []
    DataY = []

    # ---------------- POSITIVES ----------------
    pos_images = []
    for filetype in filesTypes:
        pos_images.extend(glob.glob(os.path.join(directorypathpos, "*." + filetype)))

    for path in pos_images:

        print("Loading POSITIVE:", path)

        try:
            obj = Imagehandler(path)
        except ValueError as e:
            print("POSITIVE LOAD FAILED:", e)
            continue

        try:
            HogVector = obj.ImagesToTiles(16, 16)
        except Exception as e:
            print("POSITIVE HOG FAILED:", path, e)
            continue

        for _ in range(10):
            DataX.append(HogVector)
            DataY.append(1)

    # ---------------- NEGATIVES ----------------
    neg_images = []
    for filetype in filesTypes:
        neg_images.extend(glob.glob(os.path.join(directorypathneg, "*." + filetype)))

    for path in neg_images:

        print("Loading NEGATIVE:", path)

        orig_img = cv.imread(path, cv.IMREAD_UNCHANGED)

        if orig_img is None:
            print("NEGATIVE LOAD FAILED:", path)
            continue

        h, w = orig_img.shape[:2]

        if h < 160 or w < 96:
            print("Skipping small negative:", path)
            continue

        try:
            rand_y = random.randint(0, h - 160)
            rand_x = random.randint(0, w - 96)
        except ValueError:
            continue

        patch = orig_img[rand_y:rand_y + 160, rand_x:rand_x + 96]

        try:
            obj = Imagehandler(path, patch)
        except ValueError as e:
            print("NEGATIVE PATCH FAILED:", e)
            continue

        try:
            HogVector = obj.ImagesToTiles(16, 16)
        except Exception as e:
            print("NEGATIVE HOG FAILED:", path, e)
            continue

        for _ in range(10):
            DataX.append(HogVector)
            DataY.append(0)   # ✅ CORRECT CLASS

    # ---------------- DATASET CHECK ----------------
    print("\nTotal samples:", len(DataY))
    print("Class distribution:", {0: DataY.count(0), 1: DataY.count(1)})

    if len(set(DataY)) < 2:
        print("ERROR: Only one class present. Training aborted.")
        return

    # ---------------- TRAIN ----------------
    svmObj = svmClass((DataX, DataY))
    svmObj.trainData()

    # ---------------- PREDICT ----------------
    test_images = []
    for filetype in filesTypes:
        test_images.extend(glob.glob(os.path.join(output_path, "*." + filetype)))

    for path in test_images:

        print("\nPredicting:", path)

        orig_img = cv.imread(path, cv.IMREAD_UNCHANGED)

        if orig_img is None:
            print("TEST IMAGE LOAD FAILED:", path)
            continue

        imageHeight, imageWidth = orig_img.shape[:2]

        imageHeight = max(160, (imageHeight // 160) * 160)
        imageWidth = max(96,  (imageWidth  // 96)  * 96)

        resized = cv.resize(orig_img, (imageWidth, imageHeight),
                            interpolation=cv.INTER_CUBIC)

        detections = []

        for scaledImage in Pyramid(resized, 2, (128, 64)):
            
            for (x, y, window) in SlidingWindow(scaledImage, (14, 14), (160, 96)):
                

                if window.shape[:2] != (160, 96):
                    continue

                try:
                    oi = Imagehandler(path, window)
                    Hog = oi.ImagesToTiles(16, 16)
                    val = svmObj.PredictData([Hog])[0]
                    print("Confidence:", val[1])
                except Exception:
                    continue

                if val[1] > 0.8:    
                    detections.append((x, y, 160, 96))

        final_image = resized.copy()

        for (x, y, w, h) in detections:
            cv.rectangle(final_image, (x, y),
                         (x + w, y + h), (0, 255, 0), 2)

        print("Detections:", len(detections))

        cv.imshow("Final Detections", final_image)
        cv.waitKey(0)


if __name__ == "__main__":
    cam = cv.VideoCapture(0)
    App()
    cam.release()
    cv.destroyAllWindows()
