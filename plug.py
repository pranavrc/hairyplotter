#!/usr/bin/env python

import factory
import calib
import serial
import cPickle

a = calib.Calibrator()
readingList = []

port = str(raw_input("Serial Port: "))
baudrate = str(raw_input("Baud Rate: "))
ser = serial.Serial(port, baudrate)

ref = cPickle.load(open('dataset.p', 'rb'))
ref = ref.values()
#ref = zip(ref, [0] * len(ref))

while True:
    readingList = []
    count = 0
    
    while (count < a.maxVal):
        try:
            (l, r) = ser.readline().strip('\x00\r\n').strip().split(',')
            readingList.append((int(l), int(r)))
        except:
            continue
        
        count += 1
        #readingList = zip(readingList, [0] * len(readingList))
    
    scaled = factory.scale([factory.retSimilarity(readingList, ref, 1), \
                            factory.retSimilarity(readingList, ref, 2), \
                            factory.retSimilarity(readingList, ref, 3)])
        
    print factory.classify(scaled)
