#!/usr/bin/env python

"""
Writing datasets to a Pickle.
Pranav Ravichandran <me@onloop.net>
"""

import cPickle
import os
from math import sqrt

def serialize():
    dataset = []

    #datasetCount = int(input("How many data sets? "))
    datasetCount = 4

    datasetLength = int(input("Length of each dataset: "))

    positions = {1 : 'LEFT',
                 2 : 'RIGHT',
                 3 : 'TOP',
                 4 : 'BOTTOM'}

    for count in range(datasetCount):
        dataset.append([])
        print '----'
        for x in range(datasetLength):
            print "Data " + str(x + 1) + " for set " + positions[count + 1] + ": "
            data = (int(input("x - ")), int(input("y - ")))
            dataset[count].append(data)

    cPickle.dump(dataset, open('dataset.p', 'wb'))

def retSimilarity(dataset, reference, sim):
    mismatch = []
    xfilter = 0
    yfilter = 0

    for eachRefSet in range(len(reference)):
        refLength = len(reference[eachRefSet])
        mismatch.append(0)
        for pair in range(refLength):
            if sim == 1: #Taxicab
                mismatch[eachRefSet] += abs(dataset[pair][0] - reference[eachRefSet][pair][0]) + \
                                        abs(dataset[pair][1] - reference[eachRefSet][pair][1])
            elif sim == 2: #Euclidean
                mismatch[eachRefSet] += sqrt(pow(dataset[pair][0] - reference[eachRefSet][pair][0], 2) \
                                             + pow(dataset[pair][1] - reference[eachRefSet][pair][1], 2))
            elif sim == 3: #Chebyshev
                xfilter += abs(dataset[pair][0] - reference[eachRefSet][pair][0])
                yfilter += abs(dataset[pair][1] - reference[eachRefSet][pair][1])

        if sim == 3:
            mismatch[eachRefSet] = max(xfilter, yfilter)
            xfilter, yfilter = 0, 0

    return mismatch

def classify(inList):
    positions = ['LEFT', 'RIGHT', 'BOTTOM', 'TOP']
    classify = {}

    for a in range(len(inList)):
        classify[inList[a]] = positions[a]

    inList.sort()

    return classify[inList[0]]

def scale(stuff):
    scaledScore = []
    for x in range(len(stuff[0])):
        scaledScore.append(0)
        
        for y in range(len(stuff)):
            scaledScore[x] += stuff[y][x]

        scaledScore[x] /= len(stuff)

    return scaledScore

if __name__ == "__main__":
    #serialize()
    #a = cPickle.load(open('dataset.p', 'rb'))
    a = [[(1,2),(3,4)],[(7,8),(9,10)],[(-1,-2),(-3,-4)],[(4,5),(6,7)]]
    b = [(3,6),(5,6),(7,8),(9,10)]
    c = scale([retSimilarity(b, a, 1), retSimilarity(b, a, 2), retSimilarity(b, a, 3)])
    print classify(c)
