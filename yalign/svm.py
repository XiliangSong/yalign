# -*- coding: utf-8 -*-

"""
Support Vector Machine Classifier
"""

import numpy

from sklearn import svm
from simpleai.machine_learning import Classifier


class SVMClassifier(Classifier):

    def learn(self):
        vectors = []
        answers = []
        for data in self.dataset:
            vector = self.vectorize(data)
            vectors.append(vector)
            answer = self.problem.target(data)
            answers.append(answer)
        if not vectors:
            raise ValueError("Cannot train on empty set")
        self.svm = svm.SVC()
        self._SVC_hack()
        self.svm.fit(vectors, answers)

    def classify(self, data):
        self._SVC_hack()
        vector = self.vectorize(data)
        return self.svm.predict(vector)[0], 1

    def score(self, data):
        """
        True class is positive, False class is negative.
        """
        self._SVC_hack()
        vector = self.vectorize(data)
        return float(self.svm.decision_function(vector))

    def vectorize(self, data):
        vector = [attr(data) for attr in self.attributes]
        vector = numpy.array(vector)
        return vector

    def __getstate__(self):
        result = self.__dict__.copy()
        if "dataset" in result:
            del result["dataset"]
        return result

    def _SVC_hack(self):
        """
        This is a dirty hack to deal with SVC's that were pickled using version 0.13.1
        But the user is now on a later version os scikit-learn where _impl is expected.
        """
        if not hasattr(self.svm, '_impl'):
            self.svm._impl = 'c_svc'

