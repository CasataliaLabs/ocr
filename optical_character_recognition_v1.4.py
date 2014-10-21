from PIL import ImageTk, Image
import os
import cv2,sys,glob
import time
import numpy as np
import datetime
import pylab
from Tkinter import *
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
plt.ion()
cmap = cm.Greys_r
class OpticalCharacterRecognition():
	def __init__(self):
		self.logText = 'Waiting for First OCR Result'
		self.target = 0
		self.targetTime = time.time()
		self.incriment = 0
		self.startTime = 0
		self.runningTime = 0
		self.count = [0]
		self.actualTime =[time.time()]		
	def VideoDisplay(self,video):
		frame=cv2.imread('TEST_2.JPG')  #video.read()
		rgbFrame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
		return rgbFrame
	def Target(self):
		self.target = float(targetInput.get())
		self.targetHour = float(hourInput.get())
		self.targetMin = float(minInput.get())
		self.targetSec = float(secInput.get())
		self.targetTime = self.targetSec+(self.targetMin*60)+(self.targetHour*3600)+(time.time())
		
		self.startTime = time.time()
				
	def OcrDisplay(self):
		self.incriment += 1
		self.actualTime.append(time.time())
		self.count.append(self.incriment)
		
		testImage = cv2.imread('TEST_2.JPG')
		templates = np.load('digitsTemplate.npy')
		testImageGray = cv2.cvtColor(testImage,cv2.COLOR_BGR2GRAY)
		testImageBW = cv2.inRange(testImageGray,100,255,255)
		rowMean = []
		for i in range(0,testImageBW.shape[0]):
			rowMean.append(np.mean(testImageBW[i,:]))
		rowMeanArray = np.zeros(len(rowMean))
		for i in range(0,len(rowMean)):
			rowMeanArray[i]=rowMean[i]
		rowMeanArray = rowMeanArray<=250
		line = []
		threshold = True
		for i in range(0,len(rowMean)):
			if rowMeanArray[i]==threshold:
				line.append(i)
				threshold = not(threshold)
		segmentedLine = []
		for i in range(0,len(line),2):
			segmentedLine.append(testImageBW[line[i]-5:line[i+1]+5,:])
		testImageBW = cv2.inRange(testImageGray,100,255,255)
		docSet = []
		logFile = open('docset.txt') 
		docSet.append(logFile.read())
		docSetDup = ''
		for i in range(0,len(segmentedLine)):
			black = np.zeros(segmentedLine[i].shape)
			contour, hierarchy = cv2.findContours(segmentedLine[i],cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
			parents = hierarchy[0,:,3]
			outerContour = parents == 0
			indexOfOuterContour = np.where(outerContour ==True)[0]
			charecters = []
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
				correlation = []
				for i in range(0,121):
					correlation.append(np.mean(templates[:,:,i]*cropedCharBig))
				charecters.append(chr(correlation.index(np.max(correlation))+1))
				xValuesDup.sort()
			charecterSet = ''
			for i in range(0,len(xValuesDup)):
				charecterSet += charecters[xValues.index(xValuesDup[i])]
			docSet.append(charecterSet)
			docSetDup += charecterSet + '\n'
		#~ print docSetDup
		np.savetxt('docset.txt',docSet,fmt="%s")
		self.logText = docSetDup
	def ShowGui(self,video):
		label = Label(ocrWindow, text= time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(time.time()+19800)),bg='#FFFFFF' ).place(x=screenWidth-530,y=10)
		label = Label(ocrWindow, text= time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(self.targetTime+19800)),bg='#FFFFFF' ).place(x=screenWidth-530,y=30)
		
		rgbFrame=self.VideoDisplay(video)
		axesForVideo.clear()
		axesForText.clear()
		axesForPlot.clear()
		axesForVideo.imshow(rgbFrame)
		axesForText.text(1,5,self.logText)
		axesForText.axis([0,10,0,10])
		axesForPlot.plot([self.startTime,self.targetTime], [0,self.target], '-', color='g', markersize=1)
		axesForPlot.plot(self.actualTime, self.count,'-', color='r', markersize=1)
		
		canvasForGui.show()
	def StartButton(self):
		guiTimer.start()
	def StopButton(self):
		guiTimer.stop()

ocrModuleObj=OpticalCharacterRecognition()
video = None #cv2.VideoCapture(0)
#~ ret,frame=video.read()
rgbFrame = cv2.imread('TEST_2.JPG') #cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)

ocrWindow = Tk()
screenWidth=ocrWindow.winfo_screenwidth()
screenHeight=ocrWindow.winfo_screenheight()
ocrWindow.geometry(("%dx%d")%(screenWidth,screenHeight))
ocrWindow['bg'] = '#FFFFFF'
ocrWindow.title('OpticalCharacterRecognition')
#~ 
logo = ImageTk.Image.open('logo.jpeg')
logoImage = ImageTk.PhotoImage(logo)

label = Label(ocrWindow, image = logoImage).place(x=20,y=20)

ocrFigure = Figure(facecolor='#92FEF9')
axesForVideo = ocrFigure.add_subplot(221)
axesForText = ocrFigure.add_subplot(222)
axesForPlot = ocrFigure.add_subplot(223)

axesForVideo.axes.get_xaxis().set_visible(False)
axesForVideo.axes.get_yaxis().set_visible(False)

axesForText.axes.get_xaxis().set_visible(False)
axesForText.axes.get_yaxis().set_visible(False)

label = Label(ocrWindow, text="Target",bg='#FFFFFF' ).place(x=screenWidth-230,y=10)
targetInput = Entry(ocrWindow, bd=3)
targetInput.place(x=screenWidth-300,y=30)
label = Label(ocrWindow, text="Time",bg='#FFFFFF' ).place(x=screenWidth-230,y=60)
label = Label(ocrWindow, text=":",bg='#FFFFFF' ).place(x=screenWidth-200,y=80)
label = Label(ocrWindow, text=":",bg='#FFFFFF' ).place(x=screenWidth-240,y=80)
hourInput = Entry(ocrWindow, bd=2,width = 3)
hourInput.place(x=screenWidth-275,y=80)
minInput = Entry(ocrWindow, bd=2,width = 3)
minInput.place(x=screenWidth-230,y=80)
secInput = Entry(ocrWindow, bd=2,width = 3)
secInput.place(x=screenWidth-190,y=80)
axesForPlot.grid(True)

canvasForGui = FigureCanvasTkAgg(ocrFigure, master=ocrWindow)
canvasForGui.get_tk_widget().place(x=0,y=120,width=screenWidth,height=screenHeight-140)
canvasForGui.show()

guiTimer = ocrFigure.canvas.new_timer(interval=100)
guiTimer.add_callback(ocrModuleObj.ShowGui,video)

buttonStart = Button(ocrWindow, text="START", bg='white', command=ocrModuleObj.StartButton).place(x=700, y=600)
buttonOcr = Button(ocrWindow, text="OCR", bg='white', command=ocrModuleObj.OcrDisplay).place(x=800, y=600)
buttonOk = Button(ocrWindow, text="Ok", bg='white', command=ocrModuleObj.Target).place(x=screenWidth-100, y=30)
buttonClear = Button(ocrWindow, text="Clear", bg='white', command=ocrModuleObj.Target).place(x=screenWidth-100, y=80)
buttonStop = Button(ocrWindow, text="STOP", bg='white', command=ocrModuleObj.StopButton).place(x=900, y=600)
