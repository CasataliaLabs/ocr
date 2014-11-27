__author__ = 'MidhunEM'
from scipy.ndimage.morphology import binary_dilation
from scipy.misc import imread, imsave
from PIL import ImageTk, Image
import cv2,sys,glob
import time
import numpy as np
import sang
import tkMessageBox as MessageBox 
from scipy import ndimage
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import scipy.ndimage as snd
from scipy.misc import toimage
import csv
import my_functions
plt.ion()
cmap = cm.Greys_r

class ocrModule():
	def __init__(self,sangobj):
		self.templates = np.load('digitsTemplate.npy')
		self.charsOnEdge = False
		self.sangobj = sangobj
		
	def ReaderChar(self, segLine, listOfChars):
		characters = []
		corrForChar = []
		listOfChars = self.MakeListOfChars(listOfChars)
		chars = my_functions.segmenter(segLine, 0)

		for charIn in chars:
			correlation = []
			charClipped = my_functions.clipper(charIn)
			char = cv2.resize(charClipped,(100,200))
			char = char.astype('float')
			char = char/128
			char = char - 1

			for i in listOfChars:
				tmpTemplate = self.templates[:,:,i-1]
				tmpSquare = np.square(tmpTemplate)
				tmpMean = np.mean(tmpSquare)
				tmpRoot = np.sqrt(tmpMean)
				tmpTemplateNew = tmpTemplate
				if tmpRoot > 0:
					tmpTemplateNew = tmpTemplate/tmpRoot
				correlation.append(np.mean(tmpTemplateNew * char))
			indCorrMax = correlation.index(np.max(correlation))
			corrForChar.append(np.max(correlation))
			characters.append(chr(listOfChars[indCorrMax]))
		return characters

	def MakeListOfChars(self, chars):
		asciiVals = []
		for i in chars:
			asciiVals.append(ord(i)) 
		return asciiVals
sangobj=sang.sanguino()
