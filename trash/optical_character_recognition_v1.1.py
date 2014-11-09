import cv2
import pylab
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
plt.ion()
cmap = cm.Greys_r
templates = np.load('digitsTemplate.npy')
testImage = cv2.imread('TEST_2.JPG')
testImageGray = cv2.cvtColor(testImage,cv2.COLOR_BGR2GRAY)
testImageBW = cv2.inRange(testImageGray,100,255,255)
a = []
for i in range(0,testImageBW.shape[0]):
    a.append(np.mean(testImageBW[i,:]))
a1 = np.zeros(len(a))
for i in range(0,len(a)):
    a1[i]=a[i]
a1 = a1<=250
line = []
th = True
for i in range(0,len(a)):
    if a1[i]==th:
        line.append(i)
        th = not(th)
aa = []
for i in range(0,len(line),2):
    aa.append(testImageBW[line[i]-5:line[i+1]+5,:])
bb =[]
testImageBW = cv2.inRange(testImageGray,100,255,255)
for i in range(0,len(aa)):
    black = np.zeros(aa[i].shape)
    contour, hierarchy = cv2.findContours(aa[i],cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    parents = hierarchy[0,:,3]
    #~ print hierarchy
    outerContour = parents == 0
    indexOfOuterContour = np.where(outerContour ==True)[0]
    charecters = []
    for iteration in range(0,len(indexOfOuterContour)):
        cv2.drawContours(black, contour,indexOfOuterContour[iteration],(255,255,255),-1)
        innerContour = parents ==  indexOfOuterContour[iteration]
        indexOfInnererContour = np.where(innerContour ==True)[0]
        if len(indexOfInnererContour)==0:
            pass
        else:
            for iteration1 in range(0,len(indexOfInnererContour)):
                cv2.drawContours(black, contour,indexOfInnererContour[iteration1],0,-1)
        xMax = np.max(contour[indexOfOuterContour[iteration]][:,:,0])
        yMax = np.max(contour[indexOfOuterContour[iteration]][:,:,1])
        xMin = np.min(contour[indexOfOuterContour[iteration]][:,:,0])
        yMin = np.min(contour[indexOfOuterContour[iteration]][:,:,1])
        cropedChar  = black[yMin:yMax,xMin:xMax]
        cropedCharBig = cv2.resize(cropedChar,(100,200))
        cropedCharBig =cropedCharBig.astype('float')
        cropedCharBig =cropedCharBig/128
        cropedCharBig =cropedCharBig-1
        correlation = []
        for i in range(0,121):
            correlation.append(np.mean(templates[:,:,i]*cropedCharBig))
        charecters.append(chr(correlation.index(np.max(correlation))+1))
    print charecters
    print '\n'
    
    bb.append(black)
    
    
    
