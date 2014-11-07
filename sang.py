import serial
import numpy as np
from time import sleep as sleep

class sanguino():
	def __init__(self):
		self.flag = 0
		for vtr in range(0,12):
			self.tryPort='/dev/ttyUSB' +str(vtr)
			try:
				self.ser = serial.Serial(port=self.tryPort, baudrate=9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS)
				#~ print "++ found serial on " + tryPort
			except:
				pass
				#~ print "-- no serial on " + tryPort
	def checkSensorsStat(self):
		self.ser.write(np.array([1]))
		sleep(0.50)
		self.numberOfBytesInBuffer = self.ser.inWaiting() 
		self.sensorStatusArray =	self.ser.read(self.numberOfBytesInBuffer)
		print 'sensorStatusArray: ', self.sensorStatusArray
		self.sensorStatusArrayInt = [map(int, x) for x in self.sensorStatusArray]
		print 'sensorStatusArrayInt:', self.sensorStatusArrayInt	
		#~ self.flag = 0
		for i in range(0,len(self.sensorStatusArrayInt)):
			if self.sensorStatusArrayInt[i][0] == 1:
				self.flag += 1
				
			else:
				pass
		print self.flag
		if self.flag == 4:
			self.ser.write(np.array([2]))
			print 'led on'
		else:
			self.ser.write(np.array([3]))
			print 'led off'
			



