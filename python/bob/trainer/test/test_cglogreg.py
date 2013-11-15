#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Laurent El Shafey <laurent.el-shafey@idiap.ch>
# Sat Sep 1 9:43:00 2012 +0200
#
# Copyright (C) 2011-2013 Idiap Research Institute, Martigny, Switzerland

"""Test trainer package
"""

import os, sys
import unittest
import bob
import random
import numpy

class CGLogRegTest(unittest.TestCase):
  """Performs various tests for Linear Logistic Regression."""
  
  def test01_cglogreg(self):

    # Tests our LLR Trainer.
    positives = numpy.array([
      [1.,1.2,-1.],
      [2.,2.1,2.2],
      [3.,2.9,3.1],
      [4.,3.7,4.],
      [5.,5.2,4.9],
      [6.,6.1,5.9],
      [7.,7.,7.3],
      ], dtype='float64')

    negatives = numpy.array([
      [-10.,-9.2,-1.],
      [-5.,-4.1,-0.5],
      [-10.,-9.9,-1.8],
      [-5.,-5.4,-0.3],
      [-10.,-9.3,-0.7],
      [-5.,-4.5,-0.5],
      [-10.,-9.7,-1.2],
      [-5.,-4.8,-0.2],
      ], dtype='float64')

    # Expected trained machine
    #weights_ref= numpy.array([[13.5714], [19.3997], [-0.6432]])
    weights_ref= numpy.array([[1.75536], [2.69297], [-0.54142]])
    #bias_ref = numpy.array([55.3255])
    bias_ref = numpy.array([7.26999])

    # Features and expected outputs of the trained machine
    feat1 = numpy.array([1.,2.,3.])
    #out1 = 105.7668
    out1 = 12.78703
    feat2 = numpy.array([2.,3.,4.])
    #out2 = 138.0947
    out2 = 16.69394

  
    # Trains a machine (method 1)
    T = bob.trainer.CGLogRegTrainer(0.5, 1e-5, 30)
    machine1 = T.train(negatives,positives)

    # Makes sure results are good
    self.assertTrue( (abs(machine1.weights - weights_ref) < 2e-4).all() )
    self.assertTrue( (abs(machine1.biases - bias_ref) < 2e-4).all() )
    self.assertTrue( abs(machine1(feat1) - out1) < 2e-4 )
    self.assertTrue( abs(machine1(feat2) - out2) < 2e-4 )

    # Trains a machine (method 2)
    machine2 = bob.machine.LinearMachine()
    T.train(machine2, negatives, positives)

    # Makes sure results are good
    self.assertTrue( (abs(machine2.weights - weights_ref) < 2e-4).all() )
    self.assertTrue( (abs(machine2.biases - bias_ref) < 2e-4).all() )
    self.assertTrue( abs(machine2(feat1) - out1) < 2e-4 )
    self.assertTrue( abs(machine2(feat2) - out2) < 2e-4 )


    # Expected trained machine (with regularization)
    weights_ref= numpy.array([[0.54926], [0.58304], [0.06558]])
    bias_ref = numpy.array([0.27897])

    # Trains a machine (method 1)
    T = bob.trainer.CGLogRegTrainer(0.5, 1e-5, 30, 1.)
    machine1 = T.train(negatives, positives)

    # Makes sure results are good
    self.assertTrue( (abs(machine1.weights - weights_ref) < 2e-4).all() )
    self.assertTrue( (abs(machine1.biases - bias_ref) < 2e-4).all() )
