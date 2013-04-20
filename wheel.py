#!/usr/bin/env python

import factory
import calib
import serial
import cPickle

a = calib.Calibrator()
ser = serial.Serial('/dev/ttyACM0', 9600)
ser2 = serial.Serial('/dev/ttyUSB0', 9600)

ref = cPickle.load(open('datasets.p', 'rb'))
ref = ref.values()

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
        ser.write(b'4')

    ser.flushInput()
