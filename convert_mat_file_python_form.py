#~ import cv2,sys,time
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

templateMatlab = io.loadmat('template.mat')
template = templateMatlab.get('template')
digitsTempalate = template['digits']
digitsTempalate = digitsTempalate[0,0]

trainCount = template['trainCountDigits']
trainCount = trainCount[0,0]

for k in range(trainCount.shape[1]):
	if trainCount[0,k] > 0:
		print chr(k+1)
		plt.imshow(digitsTempalate[:,:,k])
		a = raw_input('Enter to Continue')
