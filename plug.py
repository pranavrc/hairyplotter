#!/usr/bin/env python

import factory
import calib
import cPickle
import serial
import gevent
import gevent.monkey
from flask import Flask, request, Response, render_template

#gevent.monkey.patch_all()
#app = Flask(__name__)

gevent.monkey.patch_all()
app = Flask(__name__)

def stream_data(ser, ref, maxVal):
    while True:
        readingList = []
        count = 0
        while (count < maxVal):
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

        yield 'data: %s\n\n' %  factory.classify(scaled)

@app.route('/stream')
def stream():
    a = calib.Calibrator()

    #port = str(raw_input("Serial Port: "))

    #baudrate = str(raw_input("Baud Rate: "))
    ser = serial.Serial('/dev/ttyACM0', 9600)

    ref = cPickle.load(open('datasets.p', 'rb'))
    ref = ref.values()

    return Response(stream_data(ser, ref, a.maxVal),
                    mimetype = 'text/event-stream')

@app.route('/')
def index():
    return render_template('client.html')

if __name__ == '__main__':
    app.run(debug = True)
