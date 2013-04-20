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
#from PyQt4.Qwt5 import *
#from PyQt4.Qwt5.qplt import *
from PIL import Image
from matplotlib import pyplot as pplt

app = QApplication([])

class Listener:
    ''' Listens on serial port and pickles data.

            Methods: listen(int, int)
    '''

    def __init__(self, lsPort = '/dev/ttyACM1', lsTimeout = 5):
        ''' Constructor.
            Params: lsPort - Port number.
                    lsTimeout - Port Activity Timeout. '''
        self.serialObj = serial.Serial(lsPort, lsTimeout)

        if self.serialObj.isOpen():
            self.serialObj.close()
        else:
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

def livePlot():
    ser = serial.Serial('/dev/ttyACM1', 9600)

    pplt.ion()

    xAxis = [0] * 50
    yAxis = [0] * 50
    pplt.axes()

    plotLine, = pplt.plot(xAxis)
    plotLine2, = pplt.plot(yAxis)
    pplt.ylim([0, 1023])

    while True:
        try:
            (l, r, _) = ser.readline().strip('\x00\r\n').strip().split(',')
        except:
            continue

        #minXAxis = float(min(xAxis)) - 10
        #maxXAxis = float(max(xAxis)) + 10

        #pplt.ylim([minXAxis, maxXAxis])

        xAxis.append(l)
        yAxis.append(r)
        del xAxis[0]
        del yAxis[0]

        plotLine.set_xdata(np.arange(len(xAxis)))
        plotLine.set_ydata(xAxis)

        plotLine2.set_xdata(np.arange(len(yAxis)))
        plotLine2.set_ydata(yAxis)

        pplt.draw()

if __name__ == '__main__':
    #listenerObj = Listener()

    # Event Loop to listen on serial port for live data feed.
    #while True:
    #   if listenerObj.listen():
    #       dataList = cPickle.load(open('read.p', 'r'))
    #       plotterObj = Plotter(scaleDown(dataList))
    #       plotterObj.plotandsave()
    livePlot()
