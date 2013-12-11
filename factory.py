#!/usr/bin/env python

import os
from math import sqrt

positions = {1 : 'BLINK',
             2 : 'UP',
             3 : 'UP-RIGHT',
             4 : 'RIGHT',
             5 : 'DOWN-RIGHT',
             6 : 'DOWN',
             7 : 'DOWN-LEFT',
             8 : 'LEFT',
             9 : 'UP-LEFT',
            10 : 'STRAIGHT'}

def retSimilarity(dataset, reference, sim):
    mismatch = []
    xfilter = 0
    yfilter = 0

    for eachRefSet in range(len(reference)):
        refLength = len(reference[eachRefSet])
        mismatch.append(0)
        firstSum, secondSum = 0, 0
        firstSumSq, secondSumSq = 0, 0
        cumulativeSum = 0

        for pair in range(refLength):
            if sim == 1: #Taxicab
                mismatch[eachRefSet] += 1 / (1 + (abs(dataset[pair][0] - reference[eachRefSet][pair][0]) + \
                                                  abs(dataset[pair][1] - reference[eachRefSet][pair][1])))

            elif sim == 2: #Euclidean
                mismatch[eachRefSet] += 1 / (1 + sqrt(pow(dataset[pair][0] - reference[eachRefSet][pair][0], 2) \
                                                      + pow(dataset[pair][1] - reference[eachRefSet][pair][1], 2)))

            elif sim == 3: #Chebyshev
                xfilter += abs(dataset[pair][0] - reference[eachRefSet][pair][0])
                yfilter += abs(dataset[pair][1] - reference[eachRefSet][pair][1])

            elif sim == 4: #Pearson
                firstSum += dataset[pair][1]
                secondSum += reference[eachRefSet][pair][1]
                firstSumSq += pow(dataset[pair][1], 2)
                secondSumSq += pow(reference[eachRefSet][pair][1], 2)

                cumulativeSum += dataset[pair][1] * reference[eachRefSet][pair][1]

        if sim == 3:
            mismatch[eachRefSet] = 1 / (1 + max(xfilter, yfilter))
            xfilter, yfilter = 0, 0

        if sim == 4:
            top = cumulativeSum - float(firstSum * secondSum / refLength)
            bottom = sqrt((firstSumSq - float(pow(firstSum, 2) / refLength)) * \
                          (secondSumSq - float(pow(secondSum, 2) / refLength)))

            if bottom == 0 or top == 0:
                mismatch[eachRefSet] = 0
            else:
                mismatch[eachRefSet] = float(top) / float(bottom)

    return mismatch

def classify(inList):
    positionDemarc = positions.values()
    classify = {}

    for a in range(len(inList)):
        classify[inList[a]] = positionDemarc[a]

    inList.sort()

    return classify[inList[-1]]

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
    #a = cPickle.load(open('datasets.p', 'rb'))
    a = [[(1,500),(3,510),(2,520),(3,530),(4,550),(5,600)]]
    b = [(100,624),(531,652),(7,11800),(9,120),(2,500),(1,602)]
    c = scale([retSimilarity(b, a, 1), retSimilarity(b, a, 2), retSimilarity(b, a, 3)])
    d = scale([retSimilarity(b, a, 4)])
    print c
    print d
    print classify(d)
    print classify(c)
