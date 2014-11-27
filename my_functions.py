__author__ = 'Midhun EM'
import cv2
import matplotlib.pyplot as plt
import numpy
import numpy as np
import matplotlib.cm as cm
import time as time
from matplotlib.figure import Figure

def segmenter(rgb, axis):
	imBw = rgb2BwAdaptive(rgb)
	sum2 = imBw.mean(axis)
	sum2Logical = sum2 > 10;
	sum2Logical = sum2Logical * 1.0
	sum2LogicalDiff = np.diff(sum2Logical)

	lineSegStarts = np.where(sum2LogicalDiff == 1)
	lineSegStops = np.where(sum2LogicalDiff == -1)
	lineSegStarts = np.matrix(lineSegStarts)
	lineSegStops = np.matrix(lineSegStops)
#~ 
	if np.size(lineSegStarts) != np.size(lineSegStops) :
		print ('lineSegStarts length is not equal to length of lineSegStops')
		return None
		#~ if np.size(lineSegStarts) == np.size(lineSegStops) :
			#~ pass
		#~ else :
			#~ plt.subplot(212)
			#~ plt.plot(sum2LogicalDiff)
#~ 
	lineSeg = []
	for k in range(np.size(lineSegStarts)):
		if axis == 1:
			lineSeg.append(imBw[lineSegStarts[0,k]:lineSegStops[0,k], :])
		else:
			lineSeg.append(imBw[:, lineSegStarts[0,k]:lineSegStops[0,k]])
	return lineSeg	

def clipper(chars):
	#~ chars = np.matrix(chars)
	charsClipped = []
	#~ for k in range(len(chars)):
	#~ for k in range(1):
	for im in chars:
		if len(np.shape(im)) <= 1:
			return chars
			#~ break
		else:
			minMax = np.where(im)
			indMin = np.min(minMax, 1)
			indMax = np.max(minMax, 1)
			im = im[indMin[0]:indMax[0], indMin[1]:indMax[1]]
			charsClipped.append(im)
		#~ except:
			#~ charsClipped.append(im)
			#~ print 'clipper failed'
	return charsClipped

def rgb2BwAdaptive(rgb):
	print 'rgb shape =', rgb.shape
	if len(rgb.shape) >= 3:
		rgb = cv2.cvtColor(rgb,cv2.COLOR_BGR2GRAY)
		imAdaBw = cv2.adaptiveThreshold(rgb,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,101, 8)
		#~ kernel=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(2,2))
		#~ imAdaBw = cv2.dilate(imAdaBw,kernel,iterations = 1)
		#~ cv2.imwrite("lumax.png", imAdaBw)
		return imAdaBw
	else:
		return rgb
