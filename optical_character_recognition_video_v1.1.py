__author__ = 'MidhunEM'
from PIL import ImageTk, Image
import os
import cv2,sys,glob
import time
import numpy as np
import sang
import datetime
import tkMessageBox as MessageBox 
import pylab
import Tkinter
from Tkinter import *
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
plt.ion()
cmap = cm.Greys_r



class ocrclick():
	def __init__(self):
		self.positions=[]
		self.positions_x=[]
		self.positions_y=[]
			
	def onclick(self,event):
		print 'button=%d, x=%d, y=%d, xdata=%f, ydata=%f'%(event.button, event.x, event.y, event.xdata, event.ydata)
		self.positions_x.append(np.round(event.xdata))
		self.positions_y.append(np.round(event.ydata))
		self.positions=np.array([self.positions_x,self.positions_y])
				
		print "positions",self.positions_x,self.positions_y
		
		if len(self.positions)>=2:
			np.savetxt('positions.txt',self.positions,fmt="%s")
			#~ top.destroy()
			guiTimervideo.start()
			
clickObj=ocrclick()

class OpticalCharacterRecognition():
	def __init__(self,clickObj):
		self.templates = np.load('digitsTemplate.npy')
		self.logText = 'Waiting for First OCR Result'
		self.target = 0
		self.targetTime = time.time()
		self.incriment = 0
		self.startTime = 0
		self.runningTime = 0
		self.count = [0]
		self.actualTime =[time.time()]	
		self.clickObj = clickObj
		self.threshold = np.loadtxt('positions.txt')
		
			
		
			
	def VideoDisplay(self,video):
		ret,frame = video.read()
		self.rgbFrame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
		threshold = self.threshold
		if len(threshold) >= 2:
			x=threshold[:][0]
			y=threshold[:][1]
			xmin=np.min(x)
			xmax=np.max(x)
			ymin=np.min(y)
			ymax=np.max(y)
			return self.rgbFrame[ymin:ymax, xmin:xmax]
		else:
			return self.rgbFrame
	def Target(self):
		self.target = float(targetInput.get())
		self.targetHour = float(hourInput.get())
		self.targetMin = float(minInput.get())
		self.targetSec = float(secInput.get())
		self.targetTime = self.targetSec+(self.targetMin*60)+(self.targetHour*3600)+(time.time())
		
		self.startTime = time.time()
	def about(self):
		MessageBox.showinfo(title="About",message="Keep the characters under the camera properly")
		return
				
	def OcrDisplay(self):
		self.incriment += 1
		self.actualTime.append(time.time())
		self.count.append(self.incriment)
		
		testImage = self.rgbFrame
		
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
		self.line = line
		for i in range(0,len(line),2):
			if (len(line)%2 == 0) and (line[0]>6) and (line[len(line)-1]<(testImageBW.shape[0]-6)):
				print 'if loop : ', i, 'line[i]: ', line[i], 
				print 'line[i+1]:', line[i+1]
				segmentedLine.append(testImageBW[line[i]-5:line[i+1]+5,:])
			else:
				ocrModuleObj.about()	
				#~ print 'Keep the characters under the camera properly'
				
				return
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
				self.cropedChar  = black[yMin:yMax,xMin:xMax]
				self.cropedCharBig = cv2.resize(self.cropedChar,(100,200))
				self.cropedCharBig =self.cropedCharBig.astype('float')
				self.cropedCharBig =self.cropedCharBig/128
				self.cropedCharBig =self.cropedCharBig-1
				correlation = []
				for i in range(0,121):
					correlation.append(np.mean(self.templates[:,:,i]*self.cropedCharBig))
				charecters.append(chr(correlation.index(np.max(correlation))+1))
				xValuesDup.sort()
			charecterSet = ''
			for i in range(0,len(xValuesDup)):
				charecterSet += charecters[xValues.index(xValuesDup[i])]
			docSet.append(charecterSet)
			docSetDup += charecterSet + '\n'
		
		np.savetxt('docset.txt',docSet,fmt="%s")
		self.logText = docSetDup
	def ShowGui(self,video):
		label = Label(ocrWindow, text= time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(time.time()+19800)),bg='#FFFFFF' ).place(x=600,y=10)
		label = Label(ocrWindow, text= time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(self.targetTime+19800)),bg='#FFFFFF' ).place(x=600,y=30)
		self.rgbFrame = self.VideoDisplay(video)
		axesForVideo.clear()
		axesForText.clear()
		axesForPlot.clear()
		axesForVideo.imshow(self.rgbFrame)
		axesForText.text(1,5,self.logText)
		axesForText.axis([0,10,0,10])
		axesForPlot.plot([self.startTime,self.targetTime], [0,self.target], '-', color='g', markersize=1)
		axesForPlot.plot(self.actualTime, self.count,'-', color='r', markersize=1)
		canvasForvideo.show()
		canvasFortext.show()
		canvasForplot.show()
	def topbutton(self):
		guiTimervideo.stop()
		top = Toplevel(master = ocrWindow)
		logotop = ImageTk.Image.open('drishtiman.jpg')
		logoImage = ImageTk.PhotoImage(logotop) 
		label = Label(top, image = logoImage).place(x=20,y=20)
		top['bg'] = '#FFFFFF'
		top.attributes("-topmost", 1)
		top.title('Region of interest')
		toplevelfigure=Figure(facecolor='#92FEF9')
		toplevelfigure.suptitle("Select Region of Interest")
		screenWidth=top.winfo_screenwidth()
		screenHeight=top.winfo_screenheight()
		top.geometry(("%dx%d")%(screenWidth,screenHeight))
		axesForFrame=toplevelfigure.add_subplot(111)
		self.threshold = [];
		self.rgbFrame = self.VideoDisplay(video)
		axesForFrame.imshow(self.rgbFrame)
		canvasForTop = FigureCanvasTkAgg(toplevelfigure, master=top)
		canvasForTop.get_tk_widget().place(x=350,y=120)
		canvasForTop.show()
		cid = toplevelfigure.canvas.mpl_connect('button_press_event',self.clickObj.onclick)
		
	def StartButton(self):
		self.threshold = np.loadtxt('positions.txt')	
		guiTimervideo.start()
	def StopButton(self):
		guiTimervideo.stop()		
devList=glob.glob('/dev/video*')
if len(devList)==0:
    sys.exit()
else:
    camPosition=int(devList[0][10])
    if not 'video' in locals():
        video = cv2.VideoCapture(camPosition)
    if not video.isOpened():
        video.open(camPosition)
    ret, frame = video.read()
    if ret == False:
        print 'error: Check if camera is connected'
        sys.exit()
        
def key(event):
	ocrModuleObj.OcrDisplay()


sangobj=sang.sanguino()
sangobj.checkSensorsStat()

ocrModuleObj=OpticalCharacterRecognition(clickObj)


rgbFrame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB) 
ocrWindow = Tk() 
screenWidth=ocrWindow.winfo_screenwidth()
screenHeight=ocrWindow.winfo_screenheight()
ocrWindow.geometry(("%dx%d")%(screenWidth,screenHeight))
ocrWindow['bg'] = '#FFFFFF'
ocrWindow.title('OpticalCharacterRecognition')

ocrFigurevideo = Figure(figsize=(4, 4), dpi=100,facecolor='#92FEF9')
ocrFigurevideo.suptitle("VIDEO")
ocrFiguretext = Figure(figsize=(4, 4), dpi=100,facecolor='#92FEF9')
ocrFiguretext.suptitle("TEXT")
ocrFigureplot = Figure(figsize=(4, 4), dpi=100,facecolor='#92FEF9')
ocrFigureplot.suptitle("PLOT")

img = Tkinter.Image("photo", file="drishtiman.gif")
ocrWindow.tk.call('wm','iconphoto',ocrWindow._w,img) 

logo = ImageTk.Image.open('logo.jpeg')
logoImage = ImageTk.PhotoImage(logo) 
label = Label(ocrWindow, image = logoImage).place(x=20,y=20)

axesForVideo = ocrFigurevideo.add_subplot(111)
axesForText = ocrFiguretext.add_subplot(111)
axesForPlot = ocrFigureplot.add_subplot(111)

axesForVideo.axes.get_xaxis().set_visible(False)
axesForVideo.axes.get_yaxis().set_visible(False)
axesForVideo.imshow(rgbFrame)

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

canvasForvideo = FigureCanvasTkAgg(ocrFigurevideo, master=ocrWindow)
canvasForvideo.get_tk_widget().place(x=10,y=140)
canvasForvideo.show()

canvasFortext = FigureCanvasTkAgg(ocrFiguretext, master=ocrWindow)
canvasFortext.get_tk_widget().place(x=470,y=140)
canvasFortext.show()

canvasForplot = FigureCanvasTkAgg(ocrFigureplot, master=ocrWindow)
canvasForplot.get_tk_widget().place(x=930,y=140)
canvasForplot.show()

guiTimervideo = ocrFigurevideo.canvas.new_timer(interval=100)
guiTimervideo.add_callback(ocrModuleObj.ShowGui,video)

guiTimertext = ocrFiguretext.canvas.new_timer(interval=100)
guiTimertext.add_callback(ocrModuleObj.ShowGui,video)

guiTimerplot= ocrFigureplot.canvas.new_timer(interval=100)
guiTimerplot.add_callback(ocrModuleObj.ShowGui,video)

#~ ocrModuleObj.StartButton()
ocrWindow.bind('<space>',  key)
 
buttonStart = Button(ocrWindow, text="START", bg='white', command=ocrModuleObj.StartButton).place(x=150, y=600)
buttonOcr = Button(ocrWindow, text="OCR", bg='white', command=ocrModuleObj.OcrDisplay).place(x=650, y=600)
buttonOk = Button(ocrWindow, text="Ok", bg='white', command=ocrModuleObj.Target).place(x=screenWidth-100, y=30)
buttonClear = Button(ocrWindow, text="Clear", bg='white', command=ocrModuleObj.Target).place(x=screenWidth-100, y=80)
buttonStop = Button(ocrWindow, text="STOP", bg='white', command=ocrModuleObj.StopButton).place(x=1100, y=600)
buttonROI=Button(ocrWindow, text="ROI( Use only when system is showing Keep the characters under the camera properly)", bg='white', command=ocrModuleObj.topbutton).place(x=700, y=700)
