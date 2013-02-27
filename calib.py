#!/usr/bin/env python

import time
import serial
import cPickle
import sys

class Calibrator:
    positions = {'BLINK' : [],
                 'UP' : [],
                 'UP-RIGHT' : [],
                 'RIGHT' : [],
                 'DOWN-RIGHT' : [],
                 'DOWN' : [],
                 'DOWN-LEFT' : [],
                 'LEFT' : [],
                 'UP-LEFT' : []}

    def __init__(self):
        self.maxVal = int(raw_input("How many values per dataset? "))
        self.calibrate(self.maxVal)
        self.store(self.positions)
        #self.acv = self.read()

    def countdown(self, bufferTime = 3, printCount = True):
        while bufferTime > 0:
            print bufferTime
            time.sleep(1)
            bufferTime -= 1
    
        return True

    def openSerialPort(self, port, baudrate):
        s = serial.Serial(port, baudrate)
        return s

    #def loopifier(count):
    #    def loopy(func):
    #        for i in range(count):
    #            func(self.positions.keys()[i])
    #    return loopy

    #@loopifier(len(self.positions))
    def calibrate(self, upper):
        serialObj = self.openSerialPort('/dev/ttyACM0', 9600)

        print 'Stabilizing serial data'
        self.countdown(3)

        for eachPos in range(len(self.positions)):
            pos = self.positions.keys()[eachPos]
            print 'When the timer ends, make the following eye gesture: %s' % pos
            self.countdown(3)

            for i in range(upper):
                self.positions[pos].append(int(serialObj.readline().strip('\x00\r\n')))

        serialObj.close()

    def store(self, dataset):
        cPickle.dump(dataset, open('dataset.p', 'wb'))

    def read(self):
        return cPickle.load(open('dataset.p', 'rb'))

if __name__ == "__main__":
    a = Calibrator()
    #print a.acv
