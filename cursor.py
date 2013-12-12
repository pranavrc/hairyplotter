#!/usr/bin/env python

from pymouse import PyMouse
from time import sleep
import factory
import calib
import serial
import cPickle

# Create a Calibrator object.
a = calib.Calibrator()

# Open up the serial port.
ser = serial.Serial('/dev/ttyACM0', 9600)

# Deserialize the stored dataset from calibration
# Extract the lists of tuples of values from the dict.
ref = cPickle.load(open('datasets.p', 'rb'))
ref = ref.values()

mouse = PyMouse()

# Screen resolution length and height.
resL, resH = mouse.screen_size()[0], mouse.screen_size()[1]
lengthCenter, heightCenter = resL/2, resH/2

# Pixels to move by. Vertical is 1 and corresponding
# horizontal for diagonal movement is calculated.
verticalMove = 1
horizontalMove = (resL/float(resH)) * verticalMove

# Place the cursor at the center of the screen initially.
mouse.move(lengthCenter, heightCenter)

# Watch for eye movements, classify and move cursor.
while True:
    readingList = []
    count = 0

    # maxVal is the size of the dataset as specified by the user.
    while (count < a.maxVal):
        try:
            (l, r, _) = ser.readline().strip('\x00\r\n').strip().split(',')
            readingList.append((int(l), int(r)))
        except:
            continue

        count += 1

    # Calculate similarity, scale and classify.
    scaled = factory.scale([factory.retSimilarity(readingList, ref, 1), \
                            factory.retSimilarity(readingList, ref, 2), \
                            factory.retSimilarity(readingList, ref, 3), \
                            factory.retSimilarity(readingList, ref, 4)])
    direction = factory.classify(scaled)
    print direction

    l, h = mouse.position()[0], mouse.position()[1]
    mouse.move(l, h)

    # Decrease or increase the vertical/horizontal position based on the
    # direction of the eyes.
    if direction == "STRAIGHT":
        pass
    elif direction == "UP":
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

    # Clear input buffer before iterating.
    ser.flushInput()
