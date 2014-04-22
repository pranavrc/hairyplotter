#!/usr/bin/env python

from sklearn import svm
import numpy as np

class SVM_Classify:
    def __init__(self, labelled):
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
        self.targets=[1,2]

        self.clf = svm.SVC()
        self.clf.fit(self.dataset, self.targets)

    def predict(self, unlabelled):
        unlabelled = np.array(unlabelled)
        unlabelled = unlabelled.flatten()

        target = self.clf.predict(unlabelled)
        return self.positions[target[0]]
