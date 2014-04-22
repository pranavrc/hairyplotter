#!/usr/bin/env python

from sklearn import svm, lda
import numpy as np

class Classify:
    def __init__(self, labelled):
        ''' Set up the dataset and target as numpy arrays. '''
        self.positions = {1 : 'BLINK',
                          2 : 'UP',
                          3 : 'UP-RIGHT',
                          4 : 'RIGHT',
                          5 : 'DOWN-RIGHT',
                          6 : 'DOWN',
                          7 : 'DOWN-LEFT',
                          8 : 'LEFT',
                          9 : 'UP-LEFT',
                         10 : 'STRAIGHT'}

        self.dataset = np.array(labelled)
        self.dataset = self.dataset.reshape((len(self.dataset), -1))
        self.targets = np.array(self.positions.keys())

        self.clf = None

    def svm_predict(self, unlabelled):
        ''' Use a Support Vector Machine for classification. '''
        self.clf = svm.SVC()
        self.clf.fit(self.dataset, self.targets)

        unlabelled = np.array(unlabelled)
        unlabelled = unlabelled.flatten()

        target = self.clf.predict(unlabelled)
        return self.positions[target[0]]

    def lda_predict(self, unlabelled):
        ''' Use Linear Discriminant Analysis for classification.
        WARNING: Will only work when we have multiple data samples
        for each dataset (i.e., two for left, two for right, etc.)'''
        self.clf = lda.LDA()
        self.clf.fit(self.dataset, self.targets)

        unlabelled = np.array(unlabelled)
        unlabelled = unlabelled.flatten()

        target = self.clf.predict(unlabelled)
        return self.positions[target[0]]
