__author__ = 'MidhunEM'
from scipy.ndimage.morphology import binary_dilation
from scipy.misc import imread, imsave
from PIL import ImageTk, Image
#~ import os
import cv2,sys,glob
import time
import numpy as np
import sang
#~ import datetime
import tkMessageBox as MessageBox 
from scipy import ndimage
#~ import matplotlib.pyplot as plt
#~ import Tkinter
#~ from Tkinter import *
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import scipy.ndimage as snd
from scipy.misc import toimage
import csv
#~ from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
#~ from matplotlib.figure import Figure
plt.ion()
cmap = cm.Greys_r

class ocrModule():
	def __init__(self,sangobj):
		#~ self.im = im
		self.templates = np.load('digitsTemplate.npy')
		#~ self.listOfChars = listOfChars
		#~ self.corrThresh = corrThresh
		self.charsOnEdge = False
		self.sangobj = sangobj
		#~ print 'testing import of ocr module'
	
	def ConvertToBW(self):
		if self.im.shape[2] > 1:
			im = cv2.cvtColor(self.im,cv2.COLOR_BGR2GRAY)
			cv2.imwrite("lumax.png", im)
			im = cv2.resize(im,(800,400))
			print 'im shape is : ', im.shape
			im = cv2.medianBlur(im,5)
			im = cv2.adaptiveThreshold(im,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
			kernel = np.ones((3,3),np.uint8)
			#~ kernel=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
			#~ im = cv2.dilate(im,kernel,iterations = 5)
			im = cv2.erode(im,kernel,iterations = 2)
			im = cv2.morphologyEx(im, cv2.MORPH_OPEN, kernel)
			self.im = im
			#~ cv2.imwrite("lumaxtrainersmall.png", im)
			return im
		#~ if self.im.max() > 1:
			#~ self.im = cv2.inRange(im,128,255,255)
			
	
	def RowSplitter(self, im):
		self.im = im
		self.ConvertToBW()
		
		#~ self.increment += 1
		#~ self.actualTime.append(time.time())
		#~ self.count.append(self.increment)
		#~ testImage = self.rgbFrame
		rowMean = []
		for i in range(0,self.im.shape[0]):
			rowMean.append(np.mean(self.im[i,:]))
			self.rowMean = rowMean
		rowMeanArray = np.zeros(len(rowMean))
		for i in range(0,len(rowMean)):
			rowMeanArray[i]=rowMean[i]
		rowMeanArray = rowMeanArray<=250
		self.rowMeanArray = rowMeanArray
		line = []
		threshold = True # a better name is flag
		for i in range(0,len(rowMean)):
			if rowMeanArray[i]==threshold:
				line.append(i)
				threshold = not(threshold)
		self.segmentedLines = []
		self.line = line
		for i in range(0,len(line),2):
			if (len(line)%2 == 0) and (line[0]>6) and (line[len(line)-1]<(self.im.shape[0]-6)):
				print 'if loop : ', i, 'line[i]: ', line[i], 
				print 'line[i+1]:', line[i+1]
				self.segmentedLines.append(self.im[line[i]-5:line[i+1]+5,:])
			else:
				self.charsOnEdge = True
			
				#~ print 'Keep the characters under the camera properly'
				#~ return
		#~ testImageBW = cv2.inRange(testImageGray,100,255,255)
	def Reader(self, segmentedLine,listOfChars):
		#~ argSegLine = np.zeros(segmentedLine.shape)
		argSegLine = segmentedLine
		argSegLine = argSegLine * 1
		listOfChars = self.MakeListOfChars(listOfChars)
		#~ for i in range(0,len(segmentedLine)):
		black = np.zeros(segmentedLine.shape)
		contour, hierarchy = cv2.findContours(argSegLine,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
		parents = hierarchy[0,:,3]
		outerContour = parents == 0
		indexOfOuterContour = np.where(outerContour ==True)[0]
		croppedCharStore=[]
		charecters = []
		
		xValues = []
		xValuesDup = []
		corrForChar = []
		
		for iteration in range(0,len(indexOfOuterContour)):
			cv2.drawContours(black, contour,indexOfOuterContour[iteration],(255,255,255),-1)
			self.black = black
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
			self.xValuesDup = xValuesDup
			self.cropedChar  = black[yMin:yMax,xMin:xMax]
			self.cropedCharBig = cv2.resize(self.cropedChar,(100,200))
			self.cropedCharBig =self.cropedCharBig.astype('float')
			self.cropedCharBig =self.cropedCharBig/128
			self.cropedCharBig =self.cropedCharBig-1
			croppedCharStore.append(self.cropedCharBig)
			self.croppedCharStore = croppedCharStore
			
			
			correlation = []
			for i in listOfChars:
				tmpTemplate = self.templates[:,:,i-1]
				tmpSquare = np.square(tmpTemplate)
				tmpMean = np.mean(tmpSquare)
				tmpRoot = np.sqrt(tmpMean)
				tmpTemplateNew = tmpTemplate
				if tmpRoot > 0:
					tmpTemplateNew = tmpTemplate/tmpRoot
					
				correlation.append(np.mean(tmpTemplateNew*self.cropedCharBig))
				#~ charecters.append(chr(correlation.index(np.max(correlation))+1))
				#~ print 'in the for loop'
			indCorrMax = correlation.index(np.max(correlation))
			corrForChar.append(np.max(correlation))
			charecters.append(chr(listOfChars[indCorrMax]))
			xValuesDup.sort()
			docSetDup = ''
			docSet = []
			characterSet = ''
			correlationMeasures = []
			logFile = open('docset.txt') 
			docSet.append(logFile.read())
			#~ print 'breaking code'
			#~ 1/0
			for i in range(0,len(xValuesDup)):
				characterSet += charecters[xValues.index(xValuesDup[i])]
				#~ print correlation
				#~ print correlationMeasures
				correlationMeasures.append(corrForChar[xValues.index(xValuesDup[i])])
		
		docSet.append(characterSet)
		docSetDup += characterSet # + '\n'
		np.savetxt('docset.txt',docSet,fmt="%s")
		self.logText = docSetDup
		return characterSet,xValuesDup
		
	#~ def Reader1(self, segmentedLine, listOfChars):
	def MakeListOfChars(self, chars):
		#~ self.alphabet = [chr(i) for i in range(ord('A'), ord('Z') + 1)]
		asciiVals = []
		for i in chars:
			asciiVals.append(ord(i)) 
		return asciiVals
sangobj=sang.sanguino()
