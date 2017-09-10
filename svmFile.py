# -*- coding: utf-8 -*-
"""
Created on Thu Sep 07 19:30:40 2017

@author: 310247467
"""

from sklearn import svm
import numpy as np

class svmClass(object):
    def __init__(self,traindata,testdata):
        self.trainingData=traindata 
        self.testData=testdata
        self.svmObject=svm.SVC(kernel='rbf',gamma=50, C=1.0)
        
    def trainData(self):
        self.svmObject.fit(self.trainingData[0],self.trainingData[1])
        
    def PredictData(self):
        predictedValue= self.svmObject.predict(self.testData[0])
        accuracy=np.sum(predictedValue==self.testData[1])/len(self.testData[1])
        return accuracy