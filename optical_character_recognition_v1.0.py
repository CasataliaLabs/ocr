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
black = np.zeros(testImageBW.shape)
contour, hierarchy = cv2.findContours(testImageBW,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
parents = hierarchy[0,:,3]
outerContour = parents == 0
indexOfOuterContour = np.where(outerContour ==True)[0]
charecters = []
xValues = []
yValues = []
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
    cropedChar  = black[yMin:yMax,xMin:xMax]
    cropedCharBig = cv2.resize(cropedChar,(100,200))
    cropedCharBig =cropedCharBig.astype('float')
    cropedCharBig =cropedCharBig/128
    cropedCharBig =cropedCharBig-1
    correlation = []
    for i in range(0,121):
        correlation.append(np.mean(templates[:,:,i]*cropedCharBig))
    charecters.append(chr(correlation.index(np.max(correlation))+1))
plt.imshow(black, cmap)
print charecters
