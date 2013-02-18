#!/usr/bin/env python

"""
Graphs values from serial port and images them.
Pranav Ravichandran <me@onloop.net>
"""

# Dependencies: pyserial, pyQt, pyQwt, numpy, PIL

import serial
import cPickle
import numpy as np
from PyQt4.Qt import *
from PyQt4.Qwt5 import *
from PyQt4.Qwt5.qplt import *
from PIL import Image

app = QApplication([])

class Listener:
	''' Listens on serial port and pickles data.

            Methods: listen(int, int)
	'''

	def __init__(self, lsPort = 'COM10', lsTimeout = 5):
		''' Constructor.
		    Params: lsPort - Port number. 
		            lsTimeout - Port Activity Timeout. '''
		self.serialObj = serial.Serial(lsPort, lsTimeout)
		self.serialObj.open()
		self.data = []

	def listen(self, countLimit = 20, byteStream = 100):
		''' Serial Port Open, Read and Pickle.
		    Params: countLimit - Number of read operations per cycle.
		            byteStream - Number of bytes to read. '''
		for counter in range(countLimit):
			if self.serialObj.isOpen():
				self.data.append(self.serialObj.read(byteStream))
			else:
				return False

		if self.data:
			cPickle.dump(self.data, open('read.p', 'wb'))
			return True
		else:
			return False

class Plotter:
	''' Plots graph from a raw data list.

	    Methods: plotandsave()
	'''
	def __init__(self, initList, saveFile = 'plot.jpg', timeScale = 5):
		''' Constructor.
		    Params: initList - List of data from the pickled listener output. 
		            saveFile - File to write the plot to.
			    timeScale - Factor to scale x-axis values. '''
		self.xParams = []
		self.yParams = []

		for x, y in enumerate(initList):
			self.xParams.append(x/timeScale)
			self.yParams.append(y)

		self.xParams = np.array(self.xParams, np.int32)
		self.yParams = np.array(self.yParams, np.int32)

		self.saveFile = saveFile

	def plotandsave(self):
		''' Plot the data. '''
		self.plot = Plot(Curve(self.xParams, self.yParams, Pen(Red, 2), "Voltage"), "Tentative eye position plot")
		QPixmap.grabWidget(self.plot).save(self.saveFile, 'jpg')
		return

def scaleDown(listToScale, origMax = 1023, modMax = 5, origMin = 0, modMin = 0):
	''' Scale a range of values from origMin:origMax to modMin:modMax. '''
	for count in range(len(listToScale)):
		origRange = origMax - origMin
		modRange = modMax - modMin
		listToScale[count] = (listToScale[count] * float(modRange) / float(origRange))

	return listToScale

def showImg(filePath = 'plot.jpg'):
	''' Open image file. '''
	img = Image.open(filepath)
	img.show()

if __name__ == '__main__':
	listenerObj = Listener()

	# Event Loop to listen on serial port for live data feed.
	while True:
		if listenerObj.listen():
			dataList = cPickle.load(open('read.p', 'r'))
			plotterObj = Plotter(scaleDown(dataList))
			plotterObj.plotandsave()
