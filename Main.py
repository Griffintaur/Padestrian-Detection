# -*- coding: utf-8 -*-
"""

@author: Ankit Singh
"""

from ImageHandler import Imagehandler
import yaml
import glob
import os

def App():
    with open("config.yml", 'r') as ymlfile:
        cfg = yaml.load(ymlfile)
    IOPlaces=cfg['Main']
    input=IOPlaces['Input']
    output=IOPlaces['Output']
    directorypath=input
    os.chdir(input)
    filesTypes=cfg['FileType']
    images=[]
    for filetype in filesTypes:
        images.extend(glob.glob("*."+filetype))
    paths=[directorypath+image for image in images]
    print xrange(len(paths))
    for i in xrange(len(paths)):
        obj=Imagehandler(paths[i])
        print(obj.ImagesToTiles(16,16))
        print "done"
    


if __name__ == "__main__":
     App()