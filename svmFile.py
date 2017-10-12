# -*- coding: utf-8 -*-
"""
Created on Thu Sep 07 19:30:40 2017

@author: 310247467
"""

from sklearn import svm
import numpy as np

class svmClass(object):
    def __init__(self,traindata):
        self.trainingData=traindata
        self.svmObject=svm.SVC(kernel='rbf',gamma=50, C=1.0,probability=True)
        
    def trainData(self):
        self.svmObject.fit(self.trainingData[0],self.trainingData[1])
        
    def PredictData(self,data):
        predictedValue= self.svmObject.predict_proba(data)
        return predictedValue
