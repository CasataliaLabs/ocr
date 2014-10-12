import cv2 as cv2 
#~ ,sys,time
import numpy as np
#~ from Tkinter import *
#~ from tkintertable.Tables import TableCanvas
#~ from tkintertable.TableModels import TableModel
import matplotlib.pyplot as plt
import matplotlib.cm as cm
#~ from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
#~ from matplotlib.figure import Figure
import scipy.io as io

plt.ion()

digitsTempalate = np.load('digitsTemplate.npy')
trainCount = np.load('trainCount.npy')

frame = cv2.imread('TEST_2.JPG')
rgbFrame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
minimumValue = np.array([128, 128, 128], np.uint8)
maximumValue = np.array([255, 255, 255], np.uint8)
bwFrame = cv2.inRange(rgbFrame, minimumValue, maximumValue)
plt.imshow(bwFrame, cmap=cm.Greys_r)

#~ for k in range(trainCount.shape[1]):
	#~ if trainCount[0,k] > 0:
		#~ print chr(k+1)
		#~ plt.imshow(digitsTempalate[:,:,k])
		#~ rawInput = raw_input('Enter to Continue')
		#~ if rawInput == 'e':
			#~ break
		
