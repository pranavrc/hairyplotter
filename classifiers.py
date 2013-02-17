#!/usr/bin/env python

from math import sqrt

def euclidean(dataset, reference, sim):
    mismatch = []

    for eachRefSet in range(len(reference)):
        mismatch.append(0)
        refLength = len(reference[eachRefSet])
        for pair in range(refLength):
            if sim == 1: #Taxicab
                mismatch[eachRefSet] += abs(dataset[pair][0] - reference[eachRefSet][pair][0]) + \
                                         abs(dataset[pair][1] - reference[eachRefSet][pair][1])
            elif sim == 2: #Euclidean
                mismatch[eachRefSet] += sqrt(pow(dataset[pair][0] - reference[eachRefSet][pair][0], 2) \
                                              + pow(dataset[pair][1] - reference[eachRefSet][pair][1], 2))
            elif sim == 3: #Chebyshev
                mismatch[eachRefSet] += max((dataset[pair][0] - reference[eachRefSet][pair][0]), \
                                         (dataset[pair][1] - reference[eachRefSet][pair][1]))

    return mismatch

if __name__ == "__main__":
    a = [[(1,2),(3,4)],[(7,8),(9,10)]]
    b = [(3,6),(5,6),(7,8),(9,10)]
    print euclidean(b, a, 3)
