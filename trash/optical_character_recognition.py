import cv2
import pylab
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
plt.ion()
cmap = cm.Greys_r

testImage = cv2.imread('TEST_2.JPG')
testImageGray = cv2.cvtColor(testImage,cv2.COLOR_BGR2GRAY)
testImageBW = cv2.inRange(testImageGray,100,255,255)
black = np.zeros(testImageBW.shape)
contour, hierarchy = cv2.findContours(testImageBW,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
parents = hierarchy[0,:,3]
outerCountour = parents == 0
indexOfouterCountour = np.where(outerCountour ==True)[0]
for iteration in range(0,len(indexOfouterCountour)):
	cv2.drawContours(black, contour,indexOfouterCountour[iteration],(255,255,255),1)
	
plt.imshow(black,cmap)
