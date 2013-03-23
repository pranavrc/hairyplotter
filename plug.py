#!/usr/bin/env python

import factory
import calib
import serial
import cPickle
import gevent
import gevent.monkey
from flask import Flask, request, Response, render_template

gevent.monkey.patch_all()
app = Flask(__name__)

a = calib.Calibrator()
readingList = []

port = str(raw_input("Serial Port: "))
baudrate = str(raw_input("Baud Rate: "))
ser = serial.Serial(port, baudrate)

ref = cPickle.load(open('datasets.p', 'rb'))
ref = ref.values()
#ref = zip(ref, [0] * len(ref))

def stream_data():
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

        yield 'data: %s\n\n' %  factory.classify(scaled)

@app.route('/stream')
def stream():
    return Response(stream_data(),
                    mimetype = 'text/event-stream')

@app.route('/')
def index():
    return render_template('client.html')

if __name__ == '__main__':
    app.run(debug = True)
