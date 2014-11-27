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
import ocr_module
import csv
from scipy import ndimage
import my_functions
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
		#~ self.actualTime =[time.time()]	
		self.actualTime =[0]	
		self.clickObj = clickObj
		self.threshold = np.loadtxt('positions.txt')
		self.ocrObj = ocr_module.ocrModule(sangobj)
		
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
			cv2.imwrite("lumax3.png", srlf.rgbFrame)
		else:
			return self.rgbFrame

	def Target(self):
		self.target = float(targetInput.get())
		self.targetHour = float(hourInput.get())
		#~ self.targetMin = float(minInput.get())
		#~ self.targetSec = float(secInput.get())
		#~ self.targetTime = self.targetSec+(self.targetMin*60)+(self.targetHour*3600)+(time.time())
		self.targetTime = self.targetHour*3600+(time.time())
		self.startTime = time.time()
	def about(self):
		MessageBox.showinfo(title="Warning",message="Keep the characters under the camera properly")
		return
	
	def OcrDisplay(self):
		sangobj.checkSensorsStat()
		ocrModuleObj.Target()
		if np.sum(sangobj.sensorStatusArrayInt) == 4:
			self.incriment += 1
			self.actualTime.append((time.time()-self.startTime)/3600)
			self.count.append(self.incriment)
			ocrWindow['bg'] = '#00FF00'
			self.ocrObj.segmentedLines = my_functions.segmenter(self.rgbFrame, 1)
			#~ self.ocrObj.RowSplitter(self.rgbFrame)
			if len(self.ocrObj.segmentedLines)==3:
				self.line0 = self.ocrObj.ReaderChar(self.ocrObj.segmentedLines[0], 'BMPN238914/-')
				self.line1 = self.ocrObj.ReaderChar(self.ocrObj.segmentedLines[1], 'LUMAX CORNGI D')
				self.line2 = self.ocrObj.ReaderChar(self.ocrObj.segmentedLines[2], 'DATE290714/')
				self.line0 = ''.join(map(str, self.line0))
				self.line1 = ''.join(map(str, self.line1))
				self.line2 = ''.join(map(str, self.line2))

				with open('test.csv','a') as fd:
					a = csv.writer(fd, delimiter=',')
					d = time.strftime("%d/%m/%Y") 
					t = time.strftime("%I:%M:%S")
					S1 = sangobj.sensorStatusArray[0]
					S2 = sangobj.sensorStatusArray[1]
					S3 = sangobj.sensorStatusArray[2]
					S4 = sangobj.sensorStatusArray[4]                                     
					#~ data = [['Date', 'Time','S1','S2','S3','S4','Line1','Line2','Line3'],
						#~ [d,t ,S1,S2,S3,S4,self.line0,self.line1,self.line2]]
					data = [[d,t ,S1,S2,S3,S4,self.line0,self.line1,self.line2]]
						
					a.writerows(data)
			
				self.logText = []
				self.logText.append(self.line0)
				self.logText.append(self.line1)
				self.logText.append(self.line2)
				self.logText = "\n".join([self.line0, self.line1,self.line2])
			else:
				print "segmented lines are not correct"
		else:
			ocrWindow['bg'] = '#FF0000'
			self.ocrObj.RowSplitter(self.rgbFrame)
			self.line0,self.xValuesDup1 = self.ocrObj.Reader(self.ocrObj.segmentedLines[0], 'BMPN238914/')
			self.line1,self.xValuesDup2 = self.ocrObj.Reader(self.ocrObj.segmentedLines[1], 'LUMAXCORNGID')
			self.line2,self.xValuesDup3 = self.ocrObj.Reader(self.ocrObj.segmentedLines[2], 'DATE12345:')
			with open('test.csv','a') as fd:
					a = csv.writer(fd, delimiter=',')
					d = time.strftime("%d/%m/%Y") 
					t = time.strftime("%I:%M:%S")
					S1 = sangobj.sensorStatusArray[0]
					S2 = sangobj.sensorStatusArray[1]
					S3 = sangobj.sensorStatusArray[2]
					S4 = sangobj.sensorStatusArray[4]
					#~ data = [['Date', 'Time','S1','S2','S3','S4','Line1','Line2','Line3'],
						#~ [d,t ,S1,S2,S3,S4,self.line0,self.line1,self.line2]]
					data = [[d,t ,S1,S2,S3,S4,self.line0,self.line1,self.line2]]
					a.writerows(data)
			print "Problem with the object"
		
		
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
		axesForPlot.plot([(self.startTime-self.startTime)/3600,(self.targetTime-self.startTime)/3600], [0,self.target], '-', color='g', markersize=1)
		axesForPlot.plot(self.actualTime, self.count,'-', color='r', markersize=1)
		canvasForvideo.show()
		canvasFortext.show()
		canvasForplot.show()

	def topbutton(self):
		guiTimervideo.stop()
		top = Toplevel(master = ocrWindow)
		#~ logotop = ImageTk.Image.open('drishtiman.jpg')
		#~ logoImage = ImageTk.PhotoImage(logotop) 
		#~ label = Label(top, image = logoImage).place(x=20,y=20)
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
        video.set(3, 800)
        video.set(4, 448)
    if not video.isOpened():
        video.open(camPosition)
    ret, frame = video.read()
    if ret == False:
        print 'error: Check if camera is connected'
        sys.exit()

        
def key(event):
	ocrModuleObj.OcrDisplay()

sangobj=sang.sanguino()
#~ sangobj.checkSensorsStat()

ocrModuleObj=OpticalCharacterRecognition(clickObj)
rgbFrame = frame
#~ rgbFrame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
ocrWindow = Tk()
email = Label(ocrWindow, text="castalialabs.com").place(x=20,y=700) 
screenWidth=ocrWindow.winfo_screenwidth()
screenHeight=ocrWindow.winfo_screenheight()
ocrWindow.geometry(("%dx%d")%(screenWidth,screenHeight))
ocrWindow['bg'] = '#FFFFFF'
ocrWindow.title('Drishtiman Traceability Management system - Lumax Cornaglia India V.1.0')

ocrFigurevideo = Figure(figsize=(4, 4), dpi=100,facecolor='#AFEEEE')
ocrFigurevideo.suptitle("VIDEO")
ocrFiguretext = Figure(figsize=(4, 4), dpi=100,facecolor='#AFEEEE')
ocrFiguretext.suptitle("TEXT")
ocrFigureplot = Figure(figsize=(4, 4), dpi=100,facecolor='#AFEEEE')
ocrFigureplot.suptitle("PLOT")

#~ img = Tkinter.Image("photo", file="drishtiman.gif")
#~ ocrWindow.tk.call('wm','iconphoto',ocrWindow._w,img) 
#~ 
#~ logo = ImageTk.Image.open('logo.jpeg')
#~ logoImage = ImageTk.PhotoImage(logo) 
#~ label = Label(ocrWindow, image = logoImage).place(x=20,y=20)

axesForVideo = ocrFigurevideo.add_subplot(111)
axesForText = ocrFiguretext.add_subplot(111)
axesForPlot = ocrFigureplot.add_subplot(111)

axesForVideo.axes.get_xaxis().set_visible(False)
axesForVideo.axes.get_yaxis().set_visible(False)
axesForVideo.imshow(rgbFrame)

axesForText.axes.get_xaxis().set_visible(False)
axesForText.axes.get_yaxis().set_visible(False)

label = Label(ocrWindow, text="Target",bg='#FFFFFF' ).place(x=1010,y=30)
targetInput = Entry(ocrWindow, bd=3,width=4)
targetInput.place(x=screenWidth-300,y=30)
targetInput.insert(0,'1000')
label = Label(ocrWindow, text="Hour",bg='#FFFFFF' ).place(x=1020,y=82)
#~ label = Label(ocrWindow, text=":",bg='#FFFFFF' ).place(x=screenWidth-200,y=80)
#~ label = Label(ocrWindow, text=":",bg='#FFFFFF' ).place(x=screenWidth-240,y=80)
hourInput = Entry(ocrWindow, bd=2,width = 3,insertofftime=0)
hourInput.place(x=screenWidth-275,y=80)
hourInput.insert(0,'8')
#~ minInput = Entry(ocrWindow, bd=2,width = 3)
#~ minInput.place(x=screenWidth-230,y=80)
#~ secInput = Entry(ocrWindow, bd=2,width = 3)
#~ secInput.place(x=screenWidth-190,y=80)
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

ocrModuleObj.StartButton()
ocrWindow.bind('<space>',  key)
 
buttonStart = Button(ocrWindow, text="START", bg='white', command=ocrModuleObj.StartButton).place(x=150, y=600)
buttonOcr = Button(ocrWindow, text="OCR", bg='white', command=ocrModuleObj.OcrDisplay).place(x=650, y=600)
buttonOk = Button(ocrWindow, text="Ok", bg='white', command=ocrModuleObj.Target).place(x=screenWidth-100, y=30)
buttonStop = Button(ocrWindow, text="STOP", bg='white', command=ocrModuleObj.StopButton).place(x=1100, y=600)
buttonROI=Button(ocrWindow, text="ROI", bg='white', command=ocrModuleObj.topbutton).place(x=700, y=700)
