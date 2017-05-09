#!/usr/bin/env python
# Andre Anjos <andre.anjos@idiap.ch>
# Sat 24 Mar 2012 18:51:21 CET 

"""Computes an ROC curve for the Iris Flower Recognition using Linear Discriminant Analysis and Bob.
"""

import bob.db.iris
import bob.learn.linear
import bob.measure
import numpy
from matplotlib import pyplot

# Training is a 3-step thing
data = bob.db.iris.data()
trainer = bob.learn.linear.FisherLDATrainer()
machine, eigen_values = trainer.train(data.values())

# A simple way to forward the data
output = {}
for key in data.keys(): output[key] = machine(data[key])

# Performance
negatives = numpy.vstack([output['setosa'], output['versicolor']])[:,0]
positives = output['virginica'][:,0]

# Plot ROC curve
bob.measure.plot.roc(negatives, positives)
pyplot.xlabel("False Virginica Acceptance (%)")
pyplot.ylabel("False Virginica Rejection (%)")
pyplot.title("ROC Curve for Virginica Classification")
pyplot.grid()
pyplot.axis([0, 5, 0, 15]) #xmin, xmax, ymin, ymax
