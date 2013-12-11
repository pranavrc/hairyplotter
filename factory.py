#!/usr/bin/env python

import os
from math import sqrt

def retSimilarity(dataset, reference, sim):
    ''' Take a dataset of live data from the Arduino,
    take the reference dataset from the Pickle, and
    calculate similarity/distance between the two.

    sim - Type of metric to use.
        1. Taxicab metric.
        2. Euclidean distance.
        3. Chebyshev distance.
        4. Pearson coefficient. '''

    mismatch = []
    xfilter = 0
    yfilter = 0

    # Iterate through the datasets in the reference (serialized data).
    for eachRefSet in range(len(reference)):
        refLength = len(reference[eachRefSet])
        mismatch.append(0)
        firstSum, secondSum = 0, 0
        firstSumSq, secondSumSq = 0, 0
        cumulativeSum = 0

        # Apply similarity metrics on each tuple of values.
        for pair in range(refLength):
            if sim == 1: #Taxicab metric: http://en.wikipedia.org/wiki/Taxicab_geometry
                mismatch[eachRefSet] += 1 / float(1 + (abs(dataset[pair][0] - reference[eachRefSet][pair][0]) + \
                                                       abs(dataset[pair][1] - reference[eachRefSet][pair][1])))

            elif sim == 2: #Euclidean distance: http://en.wikipedia.org/wiki/Euclidean_distance
                mismatch[eachRefSet] += 1 / float(1 + sqrt(pow(dataset[pair][0] - reference[eachRefSet][pair][0], 2) \
                                                           + pow(dataset[pair][1] - reference[eachRefSet][pair][1], 2)))

            elif sim == 3: #Chebyshev distance: http://en.wikipedia.org/wiki/Chebyshev_distance
                xfilter += abs(dataset[pair][0] - reference[eachRefSet][pair][0])
                yfilter += abs(dataset[pair][1] - reference[eachRefSet][pair][1])

            elif sim == 4: #Pearson coefficient: http://en.wikipedia.org/wiki/Pearson_product-moment_correlation_coefficient
                firstSum += dataset[pair][1]
                secondSum += reference[eachRefSet][pair][1]
                firstSumSq += pow(dataset[pair][1], 2)
                secondSumSq += pow(reference[eachRefSet][pair][1], 2)

                cumulativeSum += dataset[pair][1] * reference[eachRefSet][pair][1]

        # Chebyshev and Pearson metrics return lower values for higher similarity,
        # so we invert that such that they return higher values for higher similarity.
        if sim == 3:
            mismatch[eachRefSet] = 1 / float(1 + max(xfilter, yfilter))
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

def scale(list_of_lists):
    ''' Take a list of lists that contain similarity scores.
    Find the mean of all the similarity scores in the list. '''

    scaledScore = []
    for x in range(len(list_of_lists[0])):
        scaledScore.append(0)

        for y in range(len(list_of_lists)):
            scaledScore[x] += list_of_lists[y][x]

        scaledScore[x] /= len(list_of_lists)

    return scaledScore

def classify(scaled_values):
    ''' Take a list of scaled similarities and find out
    which eye position has the list of values that is closest in
    similarity to the currently acquired list of values from
    the serial port. '''

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

    positionDemarc = positions.values()
    classify = {}

    # Assign eye position to each scaled value in that order.
    for a in range(len(scaled_values)):
        classify[scaled_values[a]] = positionDemarc[a]

    scaled_values.sort()

    # Returning the eye position corresponding to highest similarity.
    return classify[scaled_values[-1]]

if __name__ == "__main__":
    a = [[(1,500),(3,510),(2,520),(3,530),(4,550),(5,600)], [(5,600),(4,550),(3,530),(2,520),(3,510),(1,500)]]
    b = [(100,624),(531,652),(7,11800),(9,120),(2,500),(1,602)]
    c = scale([retSimilarity(b, a, 1), retSimilarity(b, a, 2), retSimilarity(b, a, 3)])
    d = scale([retSimilarity(b, a, 4)])
    print classify(c)
    print classify(d)
