#!/usr/bin/env python

import factory
import calib
import serial
import cPickle
from matplotlib import pyplot as pplt
import numpy as np

a = calib.Calibrator()
ser = serial.Serial('/dev/ttyACM0', 9600)
ser2 = serial.Serial('/dev/ttyUSB0', 9600)

ref = cPickle.load(open('datasets.p', 'rb'))
ref = ref.values()

pplt.ion()

xAxis = [0] * 50
yAxis = [0] * 50
pplt.axes()

plotLine, = pplt.plot(xAxis)
plotLine2, = pplt.plot(yAxis)
pplt.ylim([0, 1023])

while True:
    readingList = []
    count = 0

    while (count < a.maxVal):
        try:
            (l, r, _) = ser.readline().strip('\x00\r\n').strip().split(',')
            readingList.append((int(l), int(r)))
        except:
            continue

        count += 1

    scaled = factory.scale([factory.retSimilarity(readingList, ref, 1), \
                            factory.retSimilarity(readingList, ref, 2), \
                            factory.retSimilarity(readingList, ref, 3)])

    direction = factory.classify(scaled)
    print direction

    if direction == "UP" or direction == "STRAIGHT":
        ser2.write(b'1')
    elif "RIGHT" in direction:
        ser2.write(b'2')
    elif "LEFT" in direction:
        ser2.write(b'3')
    elif direction == "BLINK" or direction == "DOWN":
        ser2.write(b'4')

    xAxis.append(l)
    yAxis.append(r)
    del xAxis[0]
    del yAxis[0]

    plotLine.set_xdata(np.arange(len(xAxis)))
    plotLine.set_ydata(xAxis)

    plotLine2.set_xdata(np.arange(len(yAxis)))
    plotLine2.set_ydata(yAxis)

    pplt.draw()

    ser.flushInput()
