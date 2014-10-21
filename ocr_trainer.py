import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
plt.ion()
cmap = cm.Greys_r
templates = np.load('digitsTemplate.npy')
testImage = cv2.imread('TEST_2.JPG')
testImageGray = cv2.cvtColor(testImage,cv2.COLOR_BGR2GRAY)
testImageBW = cv2.inRange(testImageGray,100,255,255)
plt.imshow(testImage, cmap)
coordinates = np.floor(plt.ginput(n=4, timeout=30, show_clicks=True, mouse_add=1, mouse_pop=3, mouse_stop=2))
xCoord = coordinates[:,0]
yCoord = coordinates[:,1]
xMin, xMax = np.min(xCoord),np.max(xCoord)
yMin, yMax = np.min(yCoord),np.max(yCoord)
segmentedCharecter = testImageBW[yMin:yMax, xMin:xMax]
black = np.zeros(segmentedCharecter.shape)
contour, hierarchy = cv2.findContours(segmentedCharecter,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
parents = hierarchy[0,:,3]
outerContour = parents == 0
indexOfOuterContour = np.where(outerContour ==True)[0]
xValues = []
xValuesDup = []
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
    xValues.append(xMin)
    xValuesDup.append(xMin)
    cropedChar  = black[yMin:yMax,xMin:xMax]
    cropedCharBig = cv2.resize(cropedChar,(100,200))
    cropedCharBig =cropedCharBig.astype('float')
    cropedCharBig =cropedCharBig/128
    cropedCharBig =cropedCharBig-1
plt.imshow(cropedCharBig, cmap)
charecterNew = raw_input("Enter the Charecter: ")
acci = ord(charecterNew)
templates[:,:,acci-1] = (0.9*templates[:,:,acci-1])+(.1*cropedCharBig)
plt.imshow(templates[:,:,acci-1],cmap)
np.save('digitsTemplate.npy',templates)
