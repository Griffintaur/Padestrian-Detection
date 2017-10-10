# -*- coding: utf-8 -*-
"""
@author: Ankit Singh
"""
import numpy as np
import random
import math

def CartesianToSphericalCoordinates(inputVector):
    x,y,z=inputVector[0],inputVector[1],inputVector[2]
    return np.array([math.degrees(math.atan2(y,x)) , math.degrees(math.asin(z)) ]).reshape(1,2)

def InverseCartesianToSphericalCoordinates(inputVector):
    q,phi=inputVector[0],inputVector[1]
    p=1
    return np.array([p*math.cos(q)*math.sin(phi) , p*math.sin(q)*math.sin(phi), p*math.cos(phi) ]).reshape(1,3)

def R_Zq(q):
       r_zq=np.array([
            [np.cos(math.radians(q)),-np.sin(math.radians(q)),0],
            [np.sin(math.radians(q)),np.cos(math.radians(q)),0],
            [0,0,1]]
            ) 
       return r_zq
   
def R_yphi(q):
    r_yphi=np.array([
            [np.cos(math.radians(q)),0,-np.sin(math.radians(q))],
            [0,1,0],
            [np.sin(math.radians(q)),0,np.cos(math.radians(q))],
            ]
            ) 
    return r_yphi
    
def ConvertWithRespectReferenceMinutiae(ToBeConvertedMinutiae,referenceMinutiae):
    x_r,y_r,z_r,q,phi=referenceMinutiae[0],referenceMinutiae[1],referenceMinutiae[2],referenceMinutiae[3],referenceMinutiae[4]
    x,y,z,q_t,phi_t=ToBeConvertedMinutiae[0],ToBeConvertedMinutiae[1],ToBeConvertedMinutiae[2],ToBeConvertedMinutiae[3],ToBeConvertedMinutiae[4]

    X=np.array([x,y,z]).reshape(3,1)
    X_reference=np.array([x_r,y_r,z_r]).reshape(3,1)
    X=X-X_reference
    r=np.sqrt(np.sum(    X*X  ))
    X=X/r
    coordinates=np.dot(R_yphi(-phi),np.dot(R_Zq(-q),X))
#    print coordinates
    angles=CartesianToSphericalCoordinates(coordinates)
#    print angles,"done"
    temp=np.dot(R_yphi(-phi), np.dot(R_Zq(-q),InverseCartesianToSphericalCoordinates([q_t,phi_t]).T)).T
#    print temp,"sfsdf"
    angles_1=CartesianToSphericalCoordinates(
            temp.reshape(3,1)
            )
#    print angles_1
    return [r,angles[0,0],angles[0,1],angles_1[0,0],angles_1[0,1]]

def DummyAlignedMethodP(p):
    #This is a dummy method 
    return [5,6,7,15.5,16.9]
def DummyAlignedMethodQ(q):
    #This is a dummy method
    return [9,4,3,45.5,36.9]
           
def CompareTwoMinutiae(p1,q1,thresh_r,thresh_s,thresh_q,thresh_g,thresh_phi):
    r_p1,r_q1=p1[0],q1[0]
    s_p1,s_q1=p1[1],q1[1]
    q_p1,q_q1=p1[2],q1[2]
    g_p1,g_q1=p1[3],q1[4]
    phi_p1,phi_q1=p1[4],q1[4]
#    print phi_p1,phi_q1
    delta_r=np.abs(r_p1 -r_q1)
    delta_s=min(np.abs(s_p1-s_q1),360-np.abs(s_p1- s_q1))
    delta_q=min(np.abs(q_p1-q_q1),360-np.abs(q_p1-q_q1))
    delta_g=np.abs(g_p1- g_q1)
    delta_phi=np.abs(phi_p1 - phi_q1)
    print delta_r,delta_s,delta_q,delta_g,delta_phi
    if delta_r < thresh_r and delta_s <thresh_s and delta_q<thresh_q and \
    delta_g <thresh_g and delta_phi <thresh_phi :
        return True
    else:
        return False
    
    
def CountingMatchingScores(m,M_p,M_q):
    return m**2/(M_p*M_q)

def Main(P,Q,P_referenceIndex,Q_referenceIndex,thresh_r,thresh_s,thresh_q,thresh_g,thresh_phi):
    P_referenceIndex=1
    Q_referenceIndex=1
    P_reference=P.pop(P_referenceIndex)
    Q_reference=Q.pop(Q_referenceIndex)
    P_reference=DummyAlignedMethodP(P_reference)
    Q_reference=DummyAlignedMethodP(Q_reference)
    ## Aligned P and Q_reference along z axes and x axes
    #convert the list P and Q into SpherialCordinates
    
    FeatureVector_P=[]
    FeatureVector_Q=[]
    for minutiae in P:
        temp_p=ConvertWithRespectReferenceMinutiae(minutiae,P_reference)
        FeatureVector_P.append(temp_p)
    for minutiae in Q:
        temp_q=ConvertWithRespectReferenceMinutiae(minutiae,Q_reference)
        FeatureVector_Q.append(temp_q)
#    print FeatureVector_P,FeatureVector_Q
    m_count=0    
    for m_1 in FeatureVector_P:
        for m_2 in FeatureVector_Q:
           output=CompareTwoMinutiae(m_1,m_2,thresh_r,thresh_s,thresh_q,thresh_g,thresh_phi) 
           if output:
               m_count +=1
    print len(FeatureVector_P),len(FeatureVector_Q)
    score=CountingMatchingScores(m_count,len(FeatureVector_P),len(FeatureVector_Q))
    
    print score

def Simulation():
    # Since I dont understand  how to construct 3D minutiae. That's why I am just radom sample to test 
    # the algorithm. Those methods will be updated once i understand them.
    P=[[random.randint(1,50),random.randint(1,50),random.randint(1,50),math.degrees(random.randint(1,50)),math.degrees(random.randint(1,50))]for i in xrange(1,500)]
    Q=[[random.randint(1,50),random.randint(1,50),random.randint(1,50),math.degrees(random.randint(1,50)),math.degrees(random.randint(1,50))]for i in xrange(1,500)]
#    print P , Q
    Main(P,Q,10,20,22,16,28,32,36)
    
    
if __name__ == "__main__":
     Simulation()