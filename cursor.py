#!/usr/bin/env python

from pymouse import PyMouse
from time import sleep
import factory
import calib
import serial
import cPickle

a = calib.Calibrator()
ser = serial.Serial('/dev/ttyACM0', 9600)

ref = cPickle.load(open('datasets.p', 'rb'))
ref = ref.values()

mouse = PyMouse()
resL, resH = mouse.screen_size()[0], mouse.screen_size()[1]
lengthCenter, heightCenter = resL/2, resH/2
verticalMove = 1
horizontalMove = (resL/resH) * verticalMove
mouse.move(lengthCenter, heightCenter)

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
    
    l, h = mouse.position()[0], mouse.position()[1]
    mouse.move(l, h)

    if direction == "UP":
        for count in range(100):
            mouse.move(l, h)
            h -= verticalMove
    elif direction == "UP-RIGHT":
        for count in range(100):
            mouse.move(l, h)
            h -= verticalMove
            l += horizontalMove
    elif direction == "RIGHT":
        for count in range(100):
            mouse.move(l, h)
            l += horizontalMove
    elif direction == "DOWN-RIGHT":
        for count in range(100):
            mouse.move(l, h)
            h += verticalMove
            l += horizontalMove
    elif direction == "DOWN":
        for count in range(100):
            mouse.move(l, h)
            h += verticalMove
    elif direction == "DOWN-LEFT":
        for count in range(100):
            mouse.move(l, h)
            h += verticalMove
            l -= horizontalMove
    elif direction == "LEFT":
        for count in range(100):
            mouse.move(l, h)
            l -= horizontalMove
    elif direction == "UP-LEFT":
        for count in range(100):
            mouse.move(l, h)
            h -= verticalMove
            l -= horizontalMove
    elif direction == "BLINK":
        l, h = mouse.position()[0], mouse.position[1]
        mouse.click(l, h, 1)
